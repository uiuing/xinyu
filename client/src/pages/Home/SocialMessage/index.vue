<template>
    <view>
        <!--消息列表页面-->
        <view class="s-leave-message" v-show="!showLoadingPage">
            <view class="s-l-list" v-for="item in dialogueList" :key="item.dialogue_id">
                <!--消息列表-->
                <view class="s-l-item" @click="openDialogue(item)">
                    <view class="s-l-l-name">
                        <view class="s-l-l-name-text">{{
                                thisName(item)
                            }}
                        </view>
                        <view class="s-l-l-name-content">{{
                              item.content_info.substring(0, 18) +' ...'
                            }}
                        </view>
                    </view>
                    <view class="s-l-unread">
                        <view>
                            <u-badge type="error" max="99" :value="item.unread_num" :showZero="false"></u-badge>
                        </view>
                        <u-icon name="arrow-right" size="24"></u-icon>
                    </view>
                </view>
            </view>
        </view>
        <u-loading-page :loading="showLoadingPage" loading-mode="semicircle"></u-loading-page>
        <view v-if="isNullData" class="null-data">
            <u-empty
                mode="message"
                text="暂时没有您的消息～"
            >
            </u-empty>
        </view>
        <content-dialogue :data="dialogueData" @callbackPageDialog="callbackPageDialog"
                          v-if="isShowDialogue"></content-dialogue>
    </view>
</template>

<script>
import ContentDialogue from "@/pages/Home/components/ContentDialogue";

export default {
    name: "SocialMessage",
    components: {ContentDialogue},
    data() {
        return {
            dialogueList: [],
            isShowDialogue: false,
            dialogueData: {},
            isNullData: false,
            showLoadingPage: true,
            internalLock:null,
        };
    },
    created() {
        // 完成初始化
        this.updateDialogueList();
        this.internalLock = setInterval(() => {
            this.updateDialogueList();
        }, 3000);
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
        callbackPageDialog() {
            this.isShowDialogue = false;
            document.getElementsByClassName("home-navigation")[0].style.display = "block";
        },
        updateDialogueList() {
            // 更新对话列表
            let ram_data = [];
            this.$http.message.userUnreadList(this.$memory.userStatus.userId).then(res => {
                let unread_num_list = res.data.data.unread_list;
                this.$http.message.getDialogueUser(this.$memory.userStatus.userId).then(res => {
                    // 将res.data.data中的数据遍历按照字段放入ram_data中
                    for (let i = 0; i < res.data.data.length; i++) {
                        // 去unread_num_list中查找是否有相同的res.data.data[i].dialogue_id如果有则赋值unread_num
                        let unread_num = 0;
                        for (let j = 0; j < unread_num_list.length; j++) {
                            if (res.data.data[i].dialogue_id == unread_num_list[j].dialogue_id) {
                                unread_num = unread_num_list[j].number_unread;
                            }
                        }
                        ram_data.push({
                            consumption_id: res.data.data[i].consumption_id,
                            consumption_nick_name: this.$utils.base64.decode(res.data.data[i].consumption_nick_name),
                            content_info: this.$utils.base64.decode(res.data.data[i].content_info),
                            content_id: res.data.data[i].content_id,
                            dialogue_id: res.data.data[i].dialogue_id,
                            production_id: res.data.data[i].production_id,
                            create_time: res.data.data[i].create_time,
                            production_nick_name: this.$utils.base64.decode(res.data.data[i].production_nick_name),
                            unread_num: unread_num
                        });
                        // ram_data 根据unread_num从大到小排序
                        ram_data.sort((a, b) => {
                            return b.unread_num - a.unread_num;
                        });
                    }
                    this.dialogueList = ram_data;
                    if (this.dialogueList.length == 0) {
                        this.isNullData = true;
                    }
                    this.showLoadingPage = false;
                });
            });
        },
        openDialogue(item) {
            this.dialogueData.nick_name = item.production_nick_name;
            this.dialogueData.content = item.content_info;
            this.dialogueData.create_time = item.create_time;
            this.dialogueData.content_id = item.content_id;
            this.dialogueData.consumption_nick_name = this.thisName(item);
            this.dialogueData.dialogue_id = item.dialogue_id;
            this.isShowDialogue = true;
            this.$http.message.userRead(this.$memory.userStatus.userId,item.dialogue_id).then(res => {
                this.updateDialogueList();
            });
        },
        beforeDestroy() {
            clearInterval(this.internalLock);
        }
    }
};
</script>

<style scoped>
.null-data {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 200px;
}

.s-leave-message {
    overflow:auto;
    margin: 10vw 10vw 10vw 10vw;
}

.s-l-list {
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 100%;
    gap: 30px;
    margin-bottom: 30px;
}

.s-l-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.s-l-unread {
    display: flex;
    height: 100%;
    align-items: center;
    gap: 10px;
}

.s-l-l-name {
    font-size: 1rem;
    color: #333333;
}

.s-l-l-name-content {
    font-size: 0.7rem;
    color: #999999;
    padding-left: 5px;
    border-left: solid 1px #e5e5e5;
    border-bottom: solid 1px #e5e5e5;
}
</style>