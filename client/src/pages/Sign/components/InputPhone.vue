<template>
    <view>
        <!-- header -->
        <view class="i-header">
            <u-navbar
                height="9vh"
            >
                <view slot="center" style="margin-top:13px">
                    <svg t="1649934962351" viewBox="0 0 1024 1024"
                         xmlns="http://www.w3.org/2000/svg"
                         p-id="625" width="60" height="60">
                        <path
                            d="M627.6 160.9c-67.5 0-127.1 33.8-160.8 86.8-33.8-53.1-93.3-86.8-160.8-86.8-106.1 0-193 86.8-193 193 0 191.4 353.8 386 353.8 386s353.8-193 353.8-386c-0.1-106.2-86.9-193-193-193z"
                            fill="#F98AAF" p-id="626"></path>
                        <path
                            d="M835.8 719H685.1l-75.3 66.2V553.5c0-36.4 33.9-66.2 75.3-66.2h150.6c41.4 0 75.3 29.8 75.3 66.2v99.3c0.1 36.4-33.8 66.2-75.2 66.2z"
                            fill="#1B85CC" p-id="627"></path>
                        <path
                            d="M744.3 790.4H598.9l-72.7 72.7V608.7c0-40 32.7-72.7 72.7-72.7h145.4c40 0 72.7 32.7 72.7 72.7v109c0 40-32.7 72.7-72.7 72.7z"
                            fill="#2196F3" p-id="628"></path>
                        <path
                            d="M628.3 667.6c0 9.4-7.6 17-17 17s-17-7.6-17-17 7.6-17 17-17 17 7.6 17 17z m60.3-17.1c-9.4 0-17 7.6-17 17s7.6 17 17 17 17-7.6 17-17c0.1-9.3-7.6-17-17-17z m76.4 0c-9.4 0-17 7.6-17 17s7.6 17 17 17 17-7.6 17-17c0-9.3-7.6-17-17-17z"
                            fill="#FFFFFF" p-id="629"></path>
                    </svg>
                </view>
                <view slot="left" @click="callbackPage">
                    <u-icon name="arrow-left" size="30"></u-icon>
                </view>
            </u-navbar>
        </view>
        <view class="i-m-input">
            <!--title-->
            <view class="i-title">
                <view>您的电话是多少？</view>
            </view>
            <!--input-->
            <u--input
                class="i-i-input"
                placeholder="请输入手机号码"
                type="number"
                border="surround"
                shape="circle"
                :value="value"
                maxlength="11"
                fontSize="18"
                focus
                readonly
            >
                <u--text
                    text="+86"
                    slot="prefix"
                    size="17"
                    margin="0 10px 0 0"
                ></u--text>
            </u--input>
        </view>
        <view>
            <u-keyboard ref="uKeyboard" mode="number" :dotDisabled="true" :overlay="false" :show="true"
                        @change="valChange" @backspace="backspace" cancelText="清空" confirmText="提交"
                        :showCancel="false" @confirm="submitPhoneNumber"
                        zIndex="1000"
            ></u-keyboard>
            <u-toast ref="uToast"></u-toast>
        </view>
    </view>
</template>

<script>
export default {
    name: "InputPhone",
    data() {
        return {
            value: '',
            submitPhoneNumberLock: true,
        };
    },
    methods: {
        // 提交手机号码
        submitPhoneNumber() {
            // submitPhoneNumber方法1800ms内不能重复提交
            if (this.submitPhoneNumberLock){
                this.submitPhoneNumberLock = false;
                setTimeout(() => {
                    this.submitPhoneNumberLock = true;
                }, 1800);
                // 中国地区电话号码校验
                const reg = /^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$/;
                if (reg.test(this.value)) {
                    this.$refs.uToast.show({
                        type: 'loading',
                        message: '正在发送验证码',
                        duration:1500,
                        complete:()=>{
                            this.$emit("submitPhoneNumber", this.value);
                        }
                    });
                } else {
                    this.$refs.uToast.show({
                        type: 'warning',
                        message: '请输入正确的手机号码',
                    });
                }
            }
        },
        // 返回上一页
        callbackPage() {
            this.$emit("callbackPage");
        },
        // 按键被点击(点击退格键不会触发此事件)
        valChange(val) {
            // 将每次按键的值拼接到value变量中，注意+=写法
            this.value += val;
        },
        // 退格键被点击
        backspace() {
            // 删除value的最后一个字符
            if (this.value.length) this.value = this.value.substr(0, this.value.length - 1);
        }
    }
};
</script>

<style scoped>
.i-header {
    position: fixed;
}

.i-m-input {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3vh;
    margin-top: 20vh;
}

.i-i-input {
    width: 300px;
    padding: 15px 22px !important;
    background-color: #EFECECC1;
    border: none;
}
</style>