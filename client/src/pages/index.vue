<template>
    <view :style="styleVar">
        <!--优先级 1 手机端保持访问-->
        <view v-if="isPhone">
            <!--优先级 2 登录进入首页-->
            <home v-if="isLogin"></home>
            <!--优先级 2 未登录进入登录界面-->
            <sign @signIn="signIn" v-else></sign>
        </view>
        <!--优先级 1 非手机端拒绝访问-->
        <view v-else class="noPhone">
            <u-empty mode="permission">
                <view class="n-p-title">暂时不支持非移动端的访问</view>
            </u-empty>
        </view>
    </view>
</template>

<script>
import home from "@/pages/Home";
import sign from "@/pages/Sign";
import MobileDetect from "mobile-detect";

export default {
    components: {
        home,
        sign
    },
    beforeCreate() {
        // 初始化用户登录状态
        this.$memory.userStatus.init();
    },
    data() {
        return {
            // 优先级 1 判断是否是手机端
            isPhone: new MobileDetect(window.navigator.userAgent).mobile(),
            // 优先级 2 判断是否登录
            isLogin: this.$memory.userStatus.isLogin,
            styleVar: {
                '--autoHeight': this.$memory.scrollerHeight + 'px'
            }
        };
    },
    methods: {
        signIn(data) {
            this.$memory.userStatus.set(data[0], btoa(encodeURI(data[1])));
            setTimeout(() =>{
                location.reload();
            },300)
        }
    }
};
</script>

<style scoped>
.noPhone {
    margin: 100px;
}

.n-p-title {
    font-size: 22px;
    color: #dc7878;
    margin: 30px;
}
</style>
