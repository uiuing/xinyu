<template>
    <view class="p-main">
        <scroll-view style="height: 100%;" scroll-y="true" v-if="!isNullData" v-show="!showLoadingPage">
            <view class="loading" v-if="!isShowDialogue">
                <u-loadmore
                    :status="isStatus"
                    @loadmore="loadmore"
                    loadmoreText="点击我刷新推荐内容"
                    nomoreText="没有更多了"
                    loadingText="加载中..."
                    :icon="true"
                    :line="true"
                />
            </view>
            <view>
                <!--s-昵称/退出登录-->
                <view class="p-contents">
                    <view class="p-content" v-for="item of contentList" :key="item.create_time"
                          @click="openDialogue(item)">
                        <view class="p-c-time">
                            <view> {{ item.create_time }}</view>
                            <u-tag text="仅老师可见" type="warning" shape="circle"
                                   v-if="item.open_permissions == 'teacher'"
                                   :plain="true"
                                   size="mini"
                            ></u-tag>
                            <view> {{ item.nick_name }}</view>
                        </view>
                        <view class="p-c-title">
                            <view v-text="item.content.substring(0, 15)">
                            </view>
                        </view>
                    </view>
                </view>
            </view>
        </scroll-view>
        <init-content-dialogue :data="dialogueData" @callbackPageDialog="isShowDialogue = false"
                               v-if="isShowDialogue"></init-content-dialogue>
        <view v-if="isNullData" class="null-data">
            <u-empty
                mode="search"
                text="没有推荐内容，您再等等看吧～"
            >
            </u-empty>
        </view>
        <u-loading-page :loading="showLoadingPage" loading-mode="semicircle"></u-loading-page>
        <view>
            <u-toast ref="uToast"></u-toast>
        </view>
    </view>
</template>

<script>

import initContentDialogue from "@/pages/Home/components/initContentDialogue";

export default {
    name: "WorldTrends",
    components: {initContentDialogue},
    data() {
        return {
            contentList: [],
            isShowDialogue: false,
            contentData: {},
            dialogueData: {},
            isNullData: false,
            isLoading: false,
            clickLoad: true,
            isStatus: "loadmore",
            showLoadingPage: true
        };
    },
    created() {
        this.updateDialogueList();
    },
    mounted() {
        document.body.style.backgroundColor = "#f8f8f8";
        document.body.style.overflowX = "hidden";
    },
    computed: {
        // 计算属性的 getter
        thisName() {
            return (item) => {
                if (item.production_id == this.$memory.userStatus.userId) {
                    return item.consumption_nick_name;
                } else {
                    return item.production_nick_name;
                }
            };
        }
    },
    methods: {
        loadmore() {
            // 三秒内只能点击一次
            if (this.clickLoad) {
                this.updateDialogueList();
                this.isStatus = "loading";
            } else {
                this.$refs.uToast.show({
                    type: 'warning',
                    message: '您刷新的太快啦～'
                });
            }
            this.clickLoad = false;
            setTimeout(() => {
                this.isStatus = "loadmore";
            }, 600);
            setTimeout(() => {
                this.clickLoad = true;
            }, 4000);
        },
        updateDialogueList() {
            // 更新对话列表
            let ram_data = [];
            this.$http.content.getRecommendContent(this.$memory.userStatus.userId).then(res => {
                // 将res.data.data中的数据遍历按照字段放入ram_data中
                for (let i = 0; i < res.data.data.length; i++) {
                    ram_data.push({
                        content: this.$utils.base64.decode(res.data.data[i].content),
                        content_id: res.data.data[i].content_id,
                        dialogue_id: res.data.data[i].dialogue_id,
                        user_id: res.data.data[i].user_id,
                        create_time: res.data.data[i].create_time,
                        nick_name: this.$utils.base64.decode(res.data.data[i].nick_name),
                        open_permissions: res.data.data[i].open_permissions
                    });
                }
                this.contentList = ram_data;
                if (this.contentList.length == 0) {
                    this.isNullData = true;
                }
                setTimeout(() => {
                    this.showLoadingPage = false;
                }, 1);
            });
        },
        openDialogue(item) {
            this.dialogueData.nick_name = item.nick_name;
            this.dialogueData.content = item.content;
            this.dialogueData.create_time = item.create_time;
            this.dialogueData.content_id = item.content_id;
            this.dialogueData.consumption_nick_name = item.nick_name;
            this.dialogueData.user_id = item.user_id;
            this.isShowDialogue = true;
        }
    },
    beforeDestroy() {
        document.body.style.backgroundColor = "#fff";
    }
};
</script>

<style scoped>
.null-data{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top:200px;
}
.p-main {
    width: 100%;
    height: 100%;
    padding-bottom: 100px;
    overflow-x: hidden;
    overflow-y: auto;
}

.p-contents {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-top: 80px;
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
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.p-c-title {
    font-size: 16px;
    color: #333;
}

.loading {
    position: fixed;
    right: 0;
    top: 0;
    left: 0;
    z-index: 9999;
    /*底部白色渐变消失*/
    background-image: linear-gradient(to bottom, rgb(248, 248, 248) 80%, rgb(248 248 248 / 23%) 100%);
    width: 100%;
    padding: 10px 0;
}
</style>