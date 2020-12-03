<template>
<footer class="footer">
    <div class="container">
        <p class="footer__title">CrossFit® is a registered trademark of CrossFit, Inc. This website is not endorsed, sponsored, or affiliated with CrossFit, Inc.</p>
        <ul class="footer__menu">
            <li class="footer__menu--li"><a href="#">ABOUT US</a></li>
            <li class="footer__menu--li"><a href="#">TERMS OF SERVICE</a></li>
            <li class="footer__menu--li"><a href="#">PRIVACY POLICY</a></li>
        </ul>
        <ul class="footer__social">
            <li class="footer__social--li">
                <a href="#">
                    <font-awesome-icon :icon="['fab', 'facebook-f']" />
                </a>
            </li>
            <li class="footer__social--li">
                <a href="#">
                    <font-awesome-icon :icon="['fab', 'instagram']" />
                </a>
            </li>
            <li class="footer__social--li">
                <a href="#">
                    <font-awesome-icon :icon="['fab', 'youtube']" />
                </a>
            </li>
            <li class="footer__social--li">
                <a href="#">
                    <font-awesome-icon :icon="['fab', 'twitter']" />
                </a>
            </li>
        </ul>
    </div>
</footer>
</template>

<script>
export default {

}
</script>

<style lang="scss" scoped>
.footer {
    padding: 50px 10px;
    background: var(--brand-color);

    &__title {
        color: var(--brand-color-two);
        text-align: center;
        font-size: 16px;
        font-weight: 500;
    }

    &__menu {
        margin: 0;
        padding: 0;
        list-style: none;
        display: flex;
        width: 100%;
        justify-content: center;
        margin-top: 25px;
        flex-wrap: wrap;

        &--li {
            margin: 5px 15px;

            a {
                font-size: 16px;
                font-weight: bold;
                color: var(--brand-color-two);
                text-decoration: none;

                &:hover {
                    color: #000
                }
            }
        }
    }

    &__social {
        margin: 0;
        padding: 0;
        list-style: none;
        display: flex;
        width: 100%;
        justify-content: center;
        margin-top: 20px;

        &--li {
            margin: 5px 10px;

            a {
                text-decoration: none;
                background: var(--brand-color-two);
                color: var(--brand-color);
                width: 50px;
                height: 50px;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 26px;
                border-radius: 50px;

                &:hover {
                    background: #000;
                }
            }
        }
    }
}
</style>
