<template>
    <view class="background-mask">
        <view class="wri-main">
            <view class="wri-header">
                <view class="wri-h-callback" @click="callbackPage">
                    <u-icon name="arrow-down" color="rgb(100 100 100)"></u-icon>
                </view>
                <view></view>
                <view></view>
                <view class="wri-h-authority" @click="setAuthority">
                    <u-button class="wri-h-authority-btn" shape="circle" :text="authority_tips" :hairline="false"
                              size="mini" :plain="true"
                              style="color:rgb(164 164 164);"
                    ></u-button>
                </view>
                <view class="wri-h-send" @click="sendContent">
                    <u-button shape="circle" text="发布" :hairline="false" color="rgb(234 234 234)"
                              style="border:none;color:rgb(164 164 164);"
                    ></u-button>
                </view>
            </view>
            <view class="wri-input">
                <u--textarea
                    placeholder="请输入内容"
                    v-model="value"
                    :border="'none'"
                    style="padding:10px 20px;caret-color: red;background-color:rgba(56,55,43,0);resize:none;overflow:scroll;"
                    maxlength="-1"
                    autoHeight
                    id="AddContentTextarea"
                    focus
                    autofocus
                ></u--textarea>
            </view>
            <u-action-sheet :actions="list" cancelText="取消" round="10" @select="selectClick"
                            @close="closeSettings"
                            :show="show"></u-action-sheet>
        </view>
        <u-toast ref="uToast"></u-toast>
    </view>
</template>

<script>

export default {
    name: "Writing",
    data() {
        return {
            value: "",
            list: [
                {
                    name: '仅对老师可见',
                    authority: 'teacher'
                },
                {
                    name: '对所有人可见',
                    authority: 'all'
                }
            ],
            show: false,
            authority: "all",
            authority_tips: "对所有人可见",
        };
    },
    created() {
        this.$memory.draftContent.init();
        this.value = this.$memory.draftContent.content;
    },
    methods: {
        setAuthority() {
            this.show = true;
        },
        selectClick(e) {
            if (e.authority == "all") {
                this.authority_tips = "对所有人可见";
                this.authority = "all";
            } else {
                this.authority_tips = "仅对老师可见";
                this.authority = "teacher";
            }
        },
        closeSettings() {
            this.show = false;
        },
        callbackPage() {
            this.$emit("callbackPage", this.value);
        },
        // 提交内容
        sendContent() {
            if (this.value.length !== 0) {
                if (this.value.length <= 3000) {
                    this.$emit("sendContent", {
                        value:this.value,
                        open_permissions:this.authority
                    });
                } else {
                    this.$refs.uToast.show({
                        type: 'warning',
                        message: '不可超过3000个字哦～'
                    });
                }
            } else {
                this.$refs.uToast.show({
                    type: 'warning',
                    message: '请输入内容哦～'
                });
            }
        }
    }
};
</script>

<style scoped>
.background-mask {
    background-color: #ffffff;
    width: 100%;
    height: 100%;
    position: fixed;
    z-index: 500;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
}

.wri-main {
    width: 100%;
    height: 100%;
    background: radial-gradient(circle, rgba(252, 227, 239, 0.8239670868347339) 0%, rgba(232, 242, 254, 0.7399334733893557) 32%, rgba(255, 231, 246, 0.6727065826330532) 47%, rgba(223, 237, 254, 0.6671043417366946) 77%, rgba(255, 255, 255, 1) 100%);
    position: fixed;
    position: fixed;
    z-index: 800;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
}

.wri-header {
    margin: 0 8vw;
    height: 10%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.wri-h-callback {
    background-color: rgb(234 234 234);
    border-radius: 50%;
    padding: 8px;
}

.wri-h-send {
    width: 15vw;
}

.wri-h-authority-btn {
}

.wri-input {
    height: 90%;
    background-color: #fff;
    margin: 0 8vw;
    border-radius: 20px 20px 0 0;
    overflow: scroll;
}
</style>