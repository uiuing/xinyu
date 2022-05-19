<template>
    <view id="bottom-msg" class="c-d-main">
        <view class="c-callbackPage" @click="callbackPage">
            <u-icon name="arrow-left" color="rgb(100 100 100)"></u-icon>
        </view>
        <view class="c-h-info">
            <view class="c-h-info-title">{{ data.nick_name }}</view>
            <view class="c-h-info-time">{{ data.create_time }}</view>
        </view>
        <view class="c-content">
            <view v-html="escapeHTML(data.content).replace(/\n/g, '<br>')"></view>
        </view>
        <view class="c-leave-message">
            <u-divider :text="data.nick_name" textPosition="left"></u-divider>
            <view v-if="isTeacher" class="c-teacher">
                <u-tag text="已认证对方为老师" type="warning" shape="circle"
                       :plain="true"
                       size="mini"
                ></u-tag>
            </view>
            <view class="c-lm-dialogue">
                <view v-for="item in dialogueData" :key="item.create_time" :class="['c-lm-item', item.send_id == user_id ? 'production':'consumption']">
                    <u-badge :isDot="true" :type="item.send_id == user_id ? 'primary':'warning'"></u-badge>
                    <view :class="['c-l-bubble', item.send_id == user_id ? '_production':'_consumption']">
                        {{ item.msg }}
                    </view>
                </view>
            </view>
        </view>
        <a href="#"></a>
        <view :class="[focus ? 'c-input-focus' : 'c-input']">
            <view class="c-i-input">
                <u--input
                    :placeholder="'回应: ' + data.nick_name"
                    border="surround"
                    v-model="value"
                    shape="circle"
                    :adjustPosition="true"
                    confirmType="send"
                    @focus="startFocus"
                    @blur="endFocus"
                    style="background-color: rgba(255,255,255,0.88);"
                    @confirm="sendMsg"
                >
                </u--input>
            </view>
        </view>
        <u-toast ref="uToast"></u-toast>
    </view>
</template>

<script>

export default {
    name: "ContentDialogue",
    props: {
        data: {
            type: Object,
            default: {}
        }
    },
    data() {
        return {
            value: "",
            focus: false,
            dialogueData:[],
            user_id: this.$memory.userStatus.userId,
            IntervalUpdate: null,
            dialogue_id: 0,
            isTeacher: false
        };
    },
    created() {
        console.log(this.$utils.base64.encode(this.data.nick_name));
        this.$http.sign.getAuthentication(this.$utils.base64.encode(this.data.nick_name)).then(res => {
            if (res.status){
                if(res.data.data.authentication == "teacher"){
                    this.isTeacher = true;
                }
            }
        }, res => {
        });
        document.getElementsByClassName("home-navigation")[0].style.display = "none";
    },
    methods: {
        escapeHTML(str) {
            return str.replace(
                /[&<>'"]/g,
                tag =>
                    ({
                        '&': '&amp;',
                        '<': '&lt;',
                        '>': '&gt;',
                        "'": '&#39;',
                        '"': '&quot;'
                    }[tag] || tag)
            );
        },
        startUpdate() {
            setTimeout(() =>{
                this.IntervalUpdate = setInterval(() => {
                    let ram_data=[];
                    this.$http.message.dialogue(this.dialogue_id).then(res => {
                        ram_data = JSON.parse(this.$utils.base64.decode(res.data.data.content));
                        if(this.dialogueData.length != ram_data.length) {
                            this.production_id = res.data.data.production_id;
                            this.consumption_id = res.data.data.consumption_id;
                            // 遍历ram_data，根据create_time排序，从小到大
                            ram_data.sort((a, b) => {
                                return a.create_time - b.create_time;
                            });
                            this.dialogueData = ram_data;
                            setTimeout(() =>{
                                let boEl = document.getElementById("bottom-msg");
                                boEl.scrollTo({
                                    top: boEl.scrollHeight + 9999999,
                                    behavior: 'smooth'
                                });
                            },100);
                        }
                    });
                }, 10000);
            }, 2000);
        },
        callbackPage() {
            this.$emit("callbackPageDialog");
        },
        startFocus() {
            let boEl = document.getElementById("bottom-msg");
            boEl.scrollTo({
                top: boEl.scrollHeight + 9999999,
                behavior: 'smooth'
            });

            this.focus = true;
        },
        endFocus() {
            this.focus = false;
            let boEl = document.getElementById("bottom-msg");
            boEl.scrollTo({
                top: boEl.scrollHeight,
                behavior: 'smooth'
            });
        },
        sendMsg() {
            if (this.value.length !== 0) {
                if (this.value.length <= 80) {
                    this.dialogueData.push({
                        msg: this.value,
                        send_id: this.user_id,
                        create_time: new Date().getTime()
                    });
                    this.value = "";
                    this.$http.message.add(this.data.user_id, this.user_id, this.data.content_id,this.$utils.base64.encode(JSON.stringify(this.dialogueData))).then(res => {
                        if(res.data.data.once) {
                            this.dialogue_id = res.data.data.dialogue_id;
                        }
                        this.updateDialogueLists();
                        this.startUpdate();
                        this.$http.message.userUnreadAdd(this.data.user_id, this.dialogue_id);
                    });
                    setTimeout(() =>{
                        let boEl = document.getElementById("bottom-msg");
                        boEl.scrollTo({
                            top: boEl.scrollHeight + 9999999,
                            behavior: 'smooth'
                        });
                    },100);
                } else {
                    this.$refs.uToast.show({
                        type: 'warning',
                        message: '不可超过80个字哦～'
                    });
                }
            } else {
                this.$refs.uToast.show({
                    type: 'warning',
                    message: '请输入内容哦～'
                });
            }
        }
    },
    beforeDestroy() {
        clearInterval(this.IntervalUpdate);
        document.getElementsByClassName("home-navigation")[0].style.display = "block";
    }
};
</script>

<style scoped>
.c-d-main {
    background-color: #ffffff;
    width: 100%;
    position: absolute;
    z-index: 901;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    overflow: auto;
}
.c-teacher {
    display: flex;
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

.c-h-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 12vh;
    padding: 0 10vw 1vw 10vw;
    height: 50px;
}

.c-h-info-title {
    font-size: 1.2rem;
    color: #333333;
}

.c-h-info-time {
    color: #999999;
    font-size: 0.7rem;
}

.c-content {
    margin: 4vw 10vw 20vw 10vw;
    font-size: 1.2rem;
    color: #333333;
    border-right: 1px dashed rgba(236, 236, 236, 0.47);
}

.c-leave-message {
    margin: 2vw 10vw 150px 10vw;
}

.c-lm-item {
    margin-bottom: 10px;
}

.production {
    display: flex;
    width: 100%;
    flex-direction: column;
    align-items: flex-end;
}

._consumption {
    background-color: #efeeee;
    color: #333333;
}

._production {
    background-color: rgba(85, 80, 232, 0.89);
    color: #ffffff;
}

.c-l-bubble {
    width: fit-content;
    word-wrap:break-word;
    word-break:break-all;
    padding: 10px;
    font-size: .8rem;
    border-radius: 10px;
}

.c-lm-dialogue {
    margin: 5vw 0 10vw 0;
}

.c-input {
    position: fixed;
    width: 100%;
    display: flex;
    bottom: 4vh;
    justify-content: center;
}

.c-input-focus {
    position: fixed;
    width: 100%;
    display: flex;
    bottom: 1vh;
    justify-content: center;
}

.c-i-input {
    width: 80%;
}
</style>