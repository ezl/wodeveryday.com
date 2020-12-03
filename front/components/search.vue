<template>
  <section class="banner">
    <div class="container">
      <div class="banner__main">
        <h2 class="banner__title"><span>FIND A GYM </span> ANYWHERE</h2>
        <div class="banner__input">
          <autocomplete :suggestions="find_locations" @search="searchLocation"></autocomplete>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
  import autocomplete from "./autocomplete";

  export default {
    name: "search",
    components: {
      autocomplete
    },
    data: () => {
      return {
        find_locations: [],
        // currentSearchText: '',
      }
    },
    methods: {
      searchLocation(data) {
        if (
          !data ||
          (data && data.length < 3))
          return

        clearTimeout(this._timerId)
        this._timerId = setTimeout(() => {
          // this.currentSearchText = data
          this.$store.dispatch('searchLocation', {search_text: data}).then(response => {
            this.find_locations = response
          })
        }, 600)


      },
    }
  }
</script>

<style lang="scss" scoped>
  .banner {
    background: url('/images/banner.jpeg');
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    height: 85vh;
    max-height: 100%;
    display: flex;
    align-items: center;
    width: 100%;
    background-blend-mode: darken;
    background-color: rgba(0, 0, 0, .5);
    padding: 25px 15px;

    &__main {
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }

    &__title {
      font-size: 50px;
      font-weight: bold;
      color: white;
      margin-bottom: 15px;

      span {
        color: var(--brand-color)
      }
    }

    &__input {
      position: relative;
      width: 50%;
      max-width: 100%;

      button.search-submit {
        background: var(--brand-color);
        border: none;
        padding: 0;
        position: absolute;
        text-align: center;
        color: #fff;
        line-height: 44px;
        height: 44px;
        width: 65px;
        top: 0;
        right: 0;
        transition: all 0.2s ease-in-out;
        border-radius: 0 5px 5px 0;
      }

      &--control {
        width: 100%;
        padding: 10px 55px 10px 10px;
        border-radius: 5px;
        border: none;
        overflow: hidden;
      }

      &--icon {
        color: var(--brand-color-two);
        font-size: 22px;
        transition: all 0.2s ease-in-out;
      }
    }

    .banner__input button:hover .banner__input--icon {
      color: white;
    }
  }

  .welcome {
    background: var(--brand-color);
    padding: 25px 15px;

    &__main {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
    }

    &__title {
      font-size: 50px;
      color: var(--brand-color-two);
      font-weight: bold;
      text-transform: uppercase;
    }

    &__text {
      padding: 20px 5px;

      p {
        margin: 0;
        padding: 0;
        font-size: 16px;
        font-weight: normal;
        color: var(--brand-color-two);
        text-align: center;
        font-weight: 500;
      }
    }

    &__lists {
      margin: 0;
      padding: 0;
      list-style: none;
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
    }

    &__sublist {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 15px 30px;

      &--icon {
        font-size: 60px;
        color: var(--brand-color-two);
      }

      p {
        margin: 0;
        padding: 0;
        font-size: 16px;
        font-weight: normal;
        color: var(--brand-color-two);
        font-weight: 500;
      }
    }
  }

  .image--section {
    padding: 20px 0;

    &__main {
      height: 400px;
      max-height: 100%;
      padding: 20px;
    }

    &__subsection {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      border: 2px solid var(--brand-color);
      height: 100%;

      &--title {
        font-size: 45px;
        color: #fff;
        text-transform: capitalize;
        padding-bottom: 15px;
        font-weight: bold;
        margin: 0;
      }

      &--button {
        border: none;
        background: var(--brand-color);
        color: var(--brand-color-two);
        font-weight: bold;
        padding: 10px 25px;
        text-transform: uppercase;
        border-radius: 10px;
        width: 160px;
        max-width: 100%;
      }
    }
  }

  .section--one {
    background: var(--brand-color-two);

    &__image-one {
      background: url('/images/img-1.jpeg');
      background-blend-mode: darken;
      background-color: rgba(0, 0, 0, .5);
      background-size: cover;
      background-position: center center;
      background-repeat: no-repeat;
    }

    &__image-two {
      background: url('/images/img-2.jpeg');
      background-blend-mode: darken;
      background-color: rgba(0, 0, 0, .5);
      background-size: cover;
      background-position: center center;
      background-repeat: no-repeat;
    }
  }

  .section--two {
    background: var(--brand-color);

    &__image-one {
      background: url('/images/img-3.jpeg');
      background-blend-mode: darken;
      background-color: rgba(0, 0, 0, .5);
      background-size: cover;
      background-position: center center;
      background-repeat: no-repeat;
    }

    &__image-two {
      background: url('/images/img-4.jpeg');
      background-blend-mode: darken;
      background-color: rgba(0, 0, 0, .5);
      background-size: cover;
      background-position: center center;
      background-repeat: no-repeat;
    }
  }

  .section--three {
    background: var(--brand-color-two);

    &__image-one {
      background: url('/images/img-5.jpeg');
      background-blend-mode: darken;
      background-color: rgba(0, 0, 0, .5);
      background-size: cover;
      background-position: center center;
      background-repeat: no-repeat;
    }

    &__image-two {
      background: url('/images/img-6.jpeg');
      background-blend-mode: darken;
      background-color: rgba(0, 0, 0, .5);
      background-size: cover;
      background-position: center center;
      background-repeat: no-repeat;
    }
  }

  @media screen and (max-width: 600px) {
    .image--section__main {
      height: 350px;
    }

    .banner__title {
      font-size: 60px;
      text-align: center;
    }

    .banner__input {
      width: 100%;
    }

    .banner {
      height: 65vh;
    }

    .image--section__subsection--title {
      font-size: 40px;
    }

  }
</style>
