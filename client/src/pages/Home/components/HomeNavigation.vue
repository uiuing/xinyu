<template>
    <view>
        <u-tabbar :value="value6" @change="name => (value6 = name)" activeColor="#000000" :fixed="true"
                  :placeholder="true"
                  :safeAreaInsetBottom="true"
        >
            <u-tabbar-item class="sss" title="写信" text="写信" icon="order" @click="toggle"></u-tabbar-item>
            <u-tabbar-item title="世界" text="世界" icon="share" @click="toggle"></u-tabbar-item>
            <u-tabbar-item title="信件" text="信件" icon="email" @click="toggle"  :badge="number_unread" :showZero="false"></u-tabbar-item>
            <u-tabbar-item title="我的" text="我的" icon="account" @click="toggle"></u-tabbar-item>
        </u-tabbar>
    </view>
</template>

<script>
export default {
    name: 'HomeNavigation',
    data() {
        return {
            value6: 0,
            number_unread: 0
        };
    },
    beforeCreate() {
        this.$http.message.getUserUnreadCount(this.$memory.userStatus.userId).then(res => {
            if(this.number_unread != res.data.data.number_unread){
                this.number_unread = res.data.data.number_unread;
            }
        });
        setInterval(() => {
            this.$http.message.getUserUnreadCount(this.$memory.userStatus.userId).then(res => {
                if(this.number_unread != res.data.data.number_unread){
                    this.number_unread = res.data.data.number_unread;
                }
            });
        }, 2500);
    },
    methods: {
        // 将需要切换的页面的地址传送给Home父组件
        toggle(e) {
            this.$emit('selectModule', e);
        }
    }
};
</script>
