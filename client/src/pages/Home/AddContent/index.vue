<template>
    <!--写信页面-->
    <view @touchmove.stop.prevent="{}" class="add-main">
        <view class="add-input" @click="startWriting">
            <view class="add-i-box">
                <u--input
                    placeholder="说你想说..."
                    border="surround"
                    class="add-i-input"
                    fontSize=".8rem"
                    id="AddContent"
                    focus
                    autofocus
                ></u--input>
            </view>
        </view>
        <view class="add-title">
            <view class="add-t-time">
                {{ toDay }}
            </view>
            <view class="add-t-tips">
                此刻，说你想说的话～
            </view>
        </view>
        <writing
            v-if="isWriting"
            @callbackPage="callbackPage"
            @sendContent="sendContent"
        ></writing>
        <u-toast ref="uToast"></u-toast>
    </view>
</template>

<script>
import Writing from "@/pages/Home/AddContent/components/Writing";

export default {
    name: "AddContent",
    components: {
        Writing
    },
    data() {
        return {
            toDay: "",
            isWriting: false
        };
    },
    mounted() {
        // 背景透明
        document.getElementsByClassName("u-tabbar__content u-border-top u-tabbar--fixed")[0].style.backgroundColor = "#ffffffc2";
    },
    beforeMount() {
        // 获取今天日期，格式为年月日 周几
        let date = new Date();
        let month = date.getMonth() + 1;
        let day = date.getDate();
        let week = date.getDay();
        let weekArr = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
        let weekStr = weekArr[week];
        this.toDay = `${month}月${day}日 ${weekStr}`;
    },
    methods: {
        startWriting() {
            document.querySelector("#AddContent > uni-view > uni-view > uni-input > div > input").focus();
            this.isWriting = true;
        },
        callbackPage(content) {
            if (content) {
                this.$refs.uToast.show({
                    type: 'loading',
                    message: '自动保存为草稿中...',
                    duration: 500,
                    complete: () => {
                        this.$memory.draftContent.set(content);
                        this.isWriting = false;
                    }
                });
            } else {
                this.isWriting = false;
            }
        },
        sendContent(content) {
            // 发送内容
            this.$refs.uToast.show({
                type: 'loading',
                message: '正在发布内容...',
                duration: 1000,
                complete: () => {
                    // 发送内容到后端
                    let loading_content = this.$utils.base64.encode(content.value);
                    // TODO 添加仅老师可见和所有人可见
                    this.$http.content.add(this.$memory.userStatus.userId, loading_content, content.open_permissions).then(res => {
                        if (res.data.status) {
                            // 清除草稿
                            this.$memory.draftContent.clear();
                            this.isWriting = false;
                        } else {
                            this.$refs.uToast.show({
                                type: 'error',
                                message: '发布失败',
                                duration: 1000,
                                complete: () => {
                                    this.isWriting = false;
                                }
                            });
                        }
                    });
                }
            });
        }
    },
    beforeDestroy() {
        // 背景不透明
        document.getElementsByClassName("u-tabbar__content u-border-top u-tabbar--fixed")[0].style.backgroundColor = "#ffffff";
    }
};
</script>

<style scoped>
.add-main {
    background: radial-gradient(circle, rgba(255, 226, 239, 1) 0%, rgba(223, 237, 254, 1) 100%);
    height: var(--autoHeight);
}

.add-i-box {
    height: 40vh;
    width: 80%;
    margin: auto;
    border-radius: 0 0 20px 20px;
    background-color: #fff;
}

.add-i-input {
    padding: 33vh 5vw 0 5vw !important;
    border: none;
    caret-color: red;
}


.add-title {
    width: 80%;
    margin: auto;
}

.add-t-time, .add-t-tips {
    margin-left: 3vw;
    line-height: 6vh;
}

.add-t-time {
    margin-top: s-;
    color: rgba(30, 13, 13, 0.56);
    font-size: .8rem;
}

.add-t-tips {
    font-size: .8rem;
}

</style>