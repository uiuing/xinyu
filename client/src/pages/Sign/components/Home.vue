<template>
    <view>
        <!-- logo -->
        <view class="s-logo">
            <view>
                <svg t="1649934962351" class="icon" viewBox="0 0 1024 1024" version="1.1"
                     xmlns="http://www.w3.org/2000/svg"
                     p-id="625" width="105" height="105">
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
            <!--标题-->
            <view class="s-l-title">
                欣语-心中之语
            </view>
        </view>
        <!--登录按钮-->
        <view class="s-in">
            <u-button @click="signIn" type="error" color="#f88aaf" shape="circle" size="large" text="手机号登录"></u-button>
        </view>
    </view>
</template>

<script>
export default {
    name: "Home",
    data() {
        return {
            //...
        };
    },
    methods: {
        // 登录
        signIn() {
            this.$emit('signIn');
        }
    }
};
</script>

<style scoped>

.s-logo {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.s-l-title {
    letter-spacing: 3px;
    color: #0000004d;
    font-size: 20px;
    text-align: center;
    font-style: italic;
    margin-top: -15px;
}

.s-in {
    width: 44vw;
    box-shadow: 3px 4px 0 0 #2196f3;
    border-radius: 100px;
}

.s-in:hover {
    box-shadow: 3px 4px 4px 0 #2196f3;
}
</style>