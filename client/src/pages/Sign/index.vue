<template>
    <view @touchmove.stop.prevent="{}">
        <!--优先级 1 确认电话方式登录-->
        <home @touchmove.stop.prevent="{}" v-if="renderStatus.Home" class="home" @signIn="renderControl().signIn()"></home>
        <!--优先级 2 输入电话发送校验码-->
        <input-phone @touchmove.stop.prevent="{}" class="input-phone" v-if="renderStatus.InputPhone"
                     @submitPhoneNumber="submitPhoneNumber"
                     @callbackPage="callbackPage().home()"></input-phone>
        <!--优先级 3 输入校验码登录-->
        <verification @touchmove.stop.prevent="{}" class="verification" v-if="renderStatus.Verification"
                      @callbackPage="callbackPage().inputPhone()"
                      @submitCode="submitCode"
                      :code="verification.code"
        ></verification>
        <u-toast ref="uToast"></u-toast>
    </view>
</template>

<script>
import Home from "@/pages/Sign/components/Home";
import InputPhone from "@/pages/Sign/components/InputPhone";
import Verification from "@/pages/Sign/components/Verification";

export default {
    name: "Sign",
    components: {
        Home,
        InputPhone,
        Verification
    },
    data() {
        return {
            renderStatus: {
                Home: true,
                InputPhone: false,
                Verification: false,
                // 判断是不是第一次登录
                isOnceSign: true
            },
            verification: {
                phoneNumber: ''
            }
        };
    },
    methods: {
        callbackPage() {
            return {
                home: () => {
                    this.renderStatus.InputPhone = false;
                    this.renderStatus.Verification = false;
                    this.renderStatus.Home = true;
                },
                inputPhone: () => {
                    this.renderStatus.Home = false;
                    this.renderStatus.Verification = false;
                    this.renderStatus.InputPhone = true;
                }
            };
        },
        renderControl() {
            return {
                signIn: () => {
                    this.renderStatus.Home = false;
                    this.renderStatus.Verification = false;
                    this.renderStatus.InputPhone = true;
                },
                verification: () => {
                    this.renderStatus.Home = false;
                    this.renderStatus.InputPhone = false;
                    this.renderStatus.Verification = true;
                }
            };
        },
        submitPhoneNumber(phoneNumber) {
            // 根据电话发送验证码
            this.verification.phoneNumber = phoneNumber;
            this.$http.sign.sendCode(this.verification.phoneNumber).then(res => {
                if (res.data.status) {
                    this.renderControl().verification();
                } else {
                    this.$refs.uToast.show({
                        type: 'warning',
                        message: '登录太多次,请明天再试～'
                    });
                }
            }).catch(err => {
                return false;
            });
        },
        submitCode(code) {
            // 判断是否为6个数字
            if (code.length == 6) {
                this.$http.sign.verifyCode(this.verification.phoneNumber, code).then(res => {
                    if (res.data.status && res.data.data.check_judgment) {
                        this.$refs.uToast.show({
                            type: 'loading',
                            message: '正在登录中...',
                            duration: 1300,
                            complete: () => {
                                this.$emit('signIn', [res.data.data.user_id, res.data.data.nick_name]);
                            }
                        });
                    } else {
                        this.$refs.uToast.show({
                            type: 'warning',
                            message: '验证码不正确！'
                        });
                    }
                }).catch(err => {
                    return false;
                });
            }else {
                this.$refs.uToast.show({
                    type: 'warning',
                    message: '请输入完整验证码～'
                });
            }
        }
    }
}
;
</script>
<style scoped>
.home, .input-phone, .verification {
    width: 100%;
    background: #fff;
    height: var(--autoHeight);
}

.home {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
}
</style>