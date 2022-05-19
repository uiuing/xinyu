<template>
    <view class="c-main">
        <view v-show="!showLoadingPage">
            <!--详情页-->
            <view v-show="!this.isShowDialogue" class="c-callbackPage" @click="callbackPage">
                <u-icon name="close" color="rgb(100 100 100)"></u-icon>
            </view>
            <view class="c-header">
                <view class="c-h-info">
                    <view class="c-h-info-title">{{ nick_name }}</view>
                    <view class="c-h-info-time">{{ data.create_time }}</view>
                </view>
                <view class="c-h-operation">
                    <u-icon name="more-dot-fill" color="rgb(100 100 100 / 44%)" size="20" @click="show = true"></u-icon>
                </view>
            </view>
            <view class="c-content">
                <view v-html="data.content.replace(/\n/g, '<br>')"></view>
            </view>
            <view class="c-leave-message">
                <view class="c-l-title">
                    <u-divider :text="leaveMessageCount+' 人回应'" textSize="15"></u-divider>
                </view>
                <view class="c-l-list" v-for="item in dialogueList" :key="item.dialogue_id">
                    <!--消息列表-->
                    <view class="c-l-item" @click="openDialogue(item)">
                        <view class="c-l-l-name">
                            {{ item.consumption_nick_name }}
                        </view>
                        <u-icon name="arrow-right"></u-icon>
                    </view>
                </view>
            </view>
        </view>
        <u-action-sheet :actions="list" cancelText="取消" round="10" @select="selectClick" @close="show = false"
                        :show="show"></u-action-sheet>
        <u-modal :show="deleteShow" title="确定要删除内容吗？"
                 @cancel="deleteShow = false" @confirm="deleteContent"
                 :showCancelButton="true" cancelColor="rgb(41, 121, 255)" confirmColor="red" confirmText="删除"></u-modal>
        <content-dialogue :data="dialogueData" @callbackPageDialog="isShowDialogue = false"
                          v-if="isShowDialogue"></content-dialogue>
        <u-loading-page :loading="showLoadingPage" loading-mode="semicircle"></u-loading-page>
    </view>
</template>

<script>
import ContentDialogue from "@/pages/Home/components/ContentDialogue";

export default {
    name: "ContentDetails",
    components: {ContentDialogue},
    props: {
        data: {
            type: Object,
            default: {}
        }
    },
    data() {
        return {
            nick_name: this.$memory.userStatus.nickName,
            list: [
                {
                    name: '删除'
                }
            ],
            show: false,
            deleteShow: false,
            leaveMessageCount: 0,
            dialogueList: [],
            isShowDialogue: false,
            dialogueData: {},
            showLoadingPage: true
        };
    },
    created() {
        document.getElementsByClassName("home-navigation")[0].style.display = "none";
        // 完成初始化
        this.updateDialogueList();
    },
    methods: {
        callbackPage() {
            this.$emit("callbackPage");
        },
        selectClick() {
            this.deleteShow = true;
        },
        deleteContent() {
            this.$emit("deleteContent", this.data.content_id);
        },
        updateDialogueList() {
            // 更新对话列表
            let ram_data = [];
            this.$http.message.getDialogueContent(this.data.content_id).then(res => {
                // 将res.data.data中的数据遍历按照字段放入ram_data中
                for (let i = 0; i < res.data.data.length; i++) {
                    ram_data.push({
                        consumption_id: res.data.data[i].consumption_id,
                        consumption_nick_name: this.$utils.base64.decode(res.data.data[i].consumption_nick_name),
                        content_id: res.data.data[i].content_id,
                        dialogue_id: res.data.data[i].dialogue_id,
                        production_id: res.data.data[i].production_id
                    });
                }
                this.dialogueList = ram_data;
                this.leaveMessageCount = res.data.data.length;
                this.showLoadingPage = false;
            });
        },
        openDialogue(item) {
            this.dialogueData.nick_name = this.nick_name;
            this.dialogueData.content = this.data.content;
            this.dialogueData.create_time = this.data.create_time;
            this.dialogueData.content_id = item.content_id;
            this.dialogueData.consumption_nick_name = item.consumption_nick_name;
            this.dialogueData.dialogue_id = item.dialogue_id;
            this.isShowDialogue = true;
        }
    },
    beforeDestroy() {
        document.getElementsByClassName("home-navigation")[0].style.display = "block";
    }
};
</script>

<style scoped>
.c-main {
    background-color: #ffffff;
    width: 100%;
    height: 100%;
    position: fixed;
    z-index: 900;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    overflow: auto;
}

.c-callbackPage {
    background-color: #ececec;
    border-radius: 50%;
    padding: 8px;
    width: 12px;
    height: 12px;
    display: flex;
    justify-content: center;
    position: fixed;
    z-index: 910;
    left: 30px;
    top: 30px;
}

.c-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin-top: 15vh;
    padding: 0 10vw 1vw 10vw;
    height: 50px;
}

.c-h-info {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 5px;
}

.c-h-info-title {
    font-size: 1rem;
    color: #333333;
}

.c-h-info-time {
    color: #999999;
    font-size: 0.7rem;
}

.c-h-operation {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    height: 50px;
    align-items: flex-start;
}

.c-content {
    margin: 4vw 10vw 30vw 10vw;
    font-size: 1.2rem;
    color: #333333;
    border-right: 1px dashed rgba(236, 236, 236, 0.47);
}

.c-leave-message {
    margin: 2vw 10vw 30vw 10vw;
}

.c-l-list {
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 100%;
    gap: 5px;
    margin-bottom: 30px;
}

.c-l-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.c-l-l-name {
    font-size: 1rem;
    color: #333333;
}
</style>