<template>
    <view class="p-main">
        <scroll-view style="height: 100%;" scroll-y="true" v-show="!showLoadingPage">
            <view>
                <!--s-/退出登录-->
                <view class="p-header" v-if="showSettings">
                    <u-icon name="setting" color="rgb(100 100 100 / 80%)" size="25" @click="openSettings"></u-icon>
                </view>
                <view class="p-title">
                    {{ nick_name }}
                </view>
                <view class="p-contents">
                    <view class="p-content" v-for="item of historyData" :key="item.create_time"
                          @click="openDetails(item)">
                        <view class="p-c-time">
                            {{ item.create_time }}
                        </view>
                        <view class="p-c-title">
                            {{ item.content_short }}
                        </view>
                    </view>
                </view>
                <view v-if="isDataNone">
                    <u-empty
                        mode="history"
                        text="暂无历史记录"
                    >
                    </u-empty>
                </view>
                <view>
                    <u-action-sheet :actions="list" cancelText="取消" round="10" @select="selectClick"
                                    @close="closeSettings"
                                    :show="show"></u-action-sheet>
                    <u-modal :show="outShow" title="确定要退出登录吗？"
                             @cancel="outShow = false" @confirm="logOut"
                             :showCancelButton="true" cancelColor="rgb(41, 121, 255)" confirmColor="red"
                             confirmText="确定"></u-modal>
                    <content-details :data="propsData" v-if="isShowDetails" @deleteContent="deleteContent"
                                     @callbackPage="callbackPage"></content-details>
                    <u-popup :show="showModifyNickname" :round="10" mode="center"
                             :customStyle="{padding:'20px'}">
                        <u--input
                            placeholder="新昵称"
                            border="surround"
                            v-model="nickName"
                        ></u--input>
                        <view style="display:flex;gap:10px; padding:20px 0 0 0">
                            <u-button type="primary" text="确定" @click="modifyNickname"></u-button>
                            <u-button type="info" text="取消" @click="showModifyNickname = false"></u-button>
                        </view>
                    </u-popup>
                    <u-toast ref="uToast"></u-toast>
                </view>
            </view>
        </scroll-view>
        <u-loading-page :loading="showLoadingPage" loading-mode="semicircle"></u-loading-page>
    </view>
</template>

<script>
import contentDetails from "@/pages/Home/components/ContentDetails";

export default {
    name: "PersonalCenter",
    components: {
        contentDetails
    },
    data() {
        return {
            list: [
                {
                    name: '修改昵称',
                    color: '#000'
                },
                {
                    name: '退出登录',
                    color: '#919191'
                }
            ],
            show: false,
            outShow: false,
            historyData: [],
            isDataNone: false,
            isShowDetails: false,
            detailsData: {},
            propsData: {},
            nick_name: this.$memory.userStatus.nickName,
            showSettings: true,
            showModifyNickname: false,
            nickName: '',
            showLoadingPage: true
        };
    },
    created() {
        this.updateHistoryData();
    },
    mounted() {
        document.body.style.backgroundColor = "#f8f8f8";
        document.body.style.overflow = "hidden";
    },
    methods: {
        /**
         * @description: 修改昵称
         */
        modifyNickname() {
            if (this.nickName.replaceAll(" ", "").length > 0) {
                // 判断nickName是否超过10个字符
                if (this.nickName.replaceAll(" ", "").length > 10) {
                    this.$refs.uToast.show({
                        type: "error",
                        position: 'top',
                        message: "不能超过10个字"
                    });
                } else {
                    this.$http.sign.modifyNickname(this.$memory.userStatus.userId, this.$utils.base64.encode(this.nickName)).then(res => {
                        if (res.data.status) {
                            // 不能包含特殊字符
                            if (/[`~!@#$%^&*()_+<>?:"{},.\/;'[\]]/img.test(this.nickName)) {
                                this.$refs.uToast.show({
                                    type: "error",
                                    position: 'top',
                                    message: "不能包含特殊字符"
                                });
                            } else {
                                // 不能为纯英文和数字
                                if (/^[a-zA-Z0-9]*$/.test(this.nickName)) {
                                    this.$refs.uToast.show({
                                        type: "error",
                                        position: 'top',
                                        message: "昵称不能为纯英文或者数字"
                                    });
                                } else {
                                    // 不能包含英文
                                    this.$memory.userStatus.nickName = this.nickName;
                                    this.showModifyNickname = false;
                                    this.nick_name = this.nickName;
                                    this.$memory.userStatus.set(this.$memory.userStatus.userId, btoa(encodeURI(this.nickName)));
                                }
                            }
                        } else {
                            this.$refs.uToast.show({
                                type: 'warning',
                                message: '该昵称已存在~',
                                position: 'top'
                            });
                        }
                    });
                }
            } else {
                this.$refs.uToast.show({
                    type: 'warning',
                    position: 'top',
                    message: '请输入昵称'
                });
            }
        },
        callbackPage() {
            this.showSettings = true;
            this.isShowDetails = false;
        },
        logOut() {
            localStorage.clear();
            location.reload();
        },
        openSettings() {
            document.getElementsByClassName("home-navigation")[0].style.display = "none";
            this.show = true;
        },
        closeSettings() {
            this.show = false;
            setTimeout(() => {
                document.getElementsByClassName("home-navigation")[0].style.display = "block";
            }, 500);
        },
        selectClick(e) {
            if (e.name == "退出登录") {
                this.outShow = true;
            } else if (e.name == "修改昵称") {
                this.showModifyNickname = true;
            }
        },
        openDetails(item) {
            this.showSettings = false;
            this.propsData = item;
            this.detailsData = item;
            this.isShowDetails = true;
        },
        updateHistoryData() {
            this.$http.content.getHistory(this.$memory.userStatus.userId).then(res => {
                if (res.data.data.length > 0) {
                    let data = res.data.data;
                    // 遍历historyData对象使用this.$utils.base64.decode 方法解析historyData对象中的content字段
                    for (let i = 0; i < data.length; i++) {
                        let content = this.$utils.base64.decode(data[i].content);
                        data[i].content = content;
                        // 缩短content字段的长度,补充...
                        if (data[i].content.length > 35) {
                            data[i].content_short = data[i].content.substring(0, 35) + " ...";
                        } else {
                            data[i].content_short = data[i].content;
                        }
                        let create_time = data[i].create_time;
                        data[i].create_time = create_time.split(":")[0] + ":" + create_time.split(":")[1];
                    }
                    this.historyData = data;
                } else {
                    this.historyData = [];
                    this.isDataNone = true;
                }
                this.showLoadingPage = false;
            });
        },
        deleteContent(content_id) {
            this.$http.content.delete(content_id).then(res => {
                this.updateHistoryData();
                this.isShowDetails = false;
            });
        }
    },
    beforeDestroy() {
        document.body.style.backgroundColor = "#fff";
    }
};
</script>

<style scoped>
.p-main {
    width: 100%;
    height: 100%;
    padding-bottom: 100px;
    overflow-x: hidden;
    overflow-y: auto;
}

.p-header {
    position: absolute;
    top: 20px;
    z-index: 999;
    right: 25px;
}

.p-title {
    width: 100%;
    display: flex;
    justify-content: center;
    margin: 80px 0 60px 0;
    font-size: 1.5rem;
}


.p-contents {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 20px;
}

.p-content {
    width: 80%;
    background-color: #fff;
    border-radius: 20px;
    padding: 20px 20px;
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.p-c-time {
    font-size: 14px;
    color: #999;
}

.p-c-title {
    font-size: 16px;
    color: #333;
}

</style>