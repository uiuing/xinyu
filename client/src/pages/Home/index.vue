<template>
    <view class="home" :style="styleVar">
        <home-logo v-if="showLogo" :style="{'opacity':opacityActive}"></home-logo>
        <view>
            <view>
                <add-content v-if="runningModule === 0"></add-content>
                <world-trends v-else-if="runningModule === 1"></world-trends>
                <social-message v-else-if="runningModule === 2"></social-message>
                <personal-center v-else-if="runningModule === 3"></personal-center>
            </view>
            <view>
                <home-navigation class="home-navigation" @selectModule="selectModule"></home-navigation>
            </view>
        </view>
    </view>
</template>

<script>
import HomeNavigation from "@/pages/Home/components/HomeNavigation";
import AddContent from "@/pages/Home/AddContent/index";
import WorldTrends from "@/pages/Home/WorldTrends/index";
import SocialMessage from "@/pages/Home/SocialMessage/index";
import PersonalCenter from "@/pages/Home/PersonalCenter/index";
import HomeLogo from "@/pages/Home/components/HomeLogo";

export default {
    name: 'Home',
    data() {
        return {
            // 正在活动的页面地址
            runningModule: 0,
            styleVar: {
                '--autoHeight': this.$memory.scrollerHeight + 'px'
            },
            showLogo: true,
            opacityActive:1
        };
    },
    beforeCreate() {
        setTimeout(() => {
            this.$http.sign.getNickName(this.$memory.userStatus.userId).then(res => {
                this.$memory.userStatus.set(this.$memory.userStatus.userId, res.data.data.nick_name);
            });
        }, 100);
        // 没过0.2秒opacityActive-0.1直到opacityActive为0
        setTimeout(() => {
            let opacityInactive = setInterval(() => {
                if (this.opacityActive > 0) {
                    this.opacityActive -= 0.05;
                } else {
                    clearInterval(opacityInactive);
                    this.showLogo = false;
                }
            },10)
        },1500);
    },
    components: {
        // HOME导航栏
        HomeNavigation,
        // 内容添加 /导航栏地址:0
        AddContent,
        // 世界动态 /导航栏地址:1
        WorldTrends,
        // 社交消息 /导航栏地址:2
        SocialMessage,
        // 个人中心 /导航栏地址:3
        PersonalCenter,
        // 首页logo
        HomeLogo
    },
    methods: {
        // 根据导航栏的的地址自动切换页面
        selectModule: function (selectModule) {
            this.runningModule = selectModule;
        }
    }
};
</script>

<style scoped>
.home {
    height: var(--autoHeight);
    overflow: auto;
}
</style>