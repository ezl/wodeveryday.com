<template>
  <main>
    <search></search>
    <section class="welcome">
      <div class="container">
        <div class="welcome__main">
          <h2 class="welcome__title">Welcome</h2>
          <div class="welcome__text">
            <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the
              industry's standard dummy text ever
              since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen
              book. It has survived not only five

              centuries, but also the leap into electronic typesetting, remaining essentially unchanged.</p>
          </div>
          <ul class="welcome__lists">
            <li>
              <div class="welcome__sublist">
                <font-awesome-icon :icon="['fas', 'globe-americas']" class="welcome__sublist--icon"/>
                <p class="welcome__list--title">Lorem Ipsum</p>
              </div>
            </li>
            <li>
              <div class="welcome__sublist">
                <font-awesome-icon :icon="['fas', 'basketball-ball']" class="welcome__sublist--icon"/>
                <p class="welcome__list--title">Lorem Ipsum</p>
              </div>
            </li>
            <li>
              <div class="welcome__sublist">
                <font-awesome-icon :icon="['fab', 'creative-commons-sampling-plus']" class="welcome__sublist--icon"/>
                <p class="welcome__list--title">Lorem Ipsum</p>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </section>
    <section class="image--section section--one">
      <div class="container">
        <div class="row">
          <div class="col-lg-6 mb-3 mb-lg-0">
            <div class="image--section__main section--one__image-one">
              <div class="image--section__subsection">
                <p class="image--section__subsection--title">ASIA</p>
                <button @click="pushContinent('asia')" class="image--section__subsection--button">Search</button>
              </div>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="image--section__main section--one__image-two">
              <div class="image--section__subsection">
                <p class="image--section__subsection--title">AFRICA</p>
                <button @click="pushContinent('africa')" class="image--section__subsection--button">Search</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section class="image--section section--two">
      <div class="container">
        <div class="row">
          <div class="col-lg-6 mb-3 mb-lg-0">
            <div class="image--section__main section--two__image-one">
              <div class="image--section__subsection">
                <p class="image--section__subsection--title">EUROPE</p>
                <button @click="pushContinent('europe')" class="image--section__subsection--button">Search</button>
              </div>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="image--section__main section--two__image-two">
              <div class="image--section__subsection">
                <p class="image--section__subsection--title">NORTH AMERICA</p>
                <button @click="pushContinent('north-america')" class="image--section__subsection--button">Search
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section class="image--section section--three">
      <div class="container">
        <div class="row">
          <div class="col-lg-6 mb-3 mb-lg-0">
            <div class="image--section__main section--three__image-one">
              <div class="image--section__subsection">
                <p class="image--section__subsection--title">SOUTH AMERICA</p>
                <button @click="pushContinent('south-america')" class="image--section__subsection--button">Search
                </button>
              </div>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="image--section__main section--three__image-two">
              <div class="image--section__subsection">
                <p class="image--section__subsection--title">OCEANIA</p>
                <button @click="pushContinent('oceania')" class="image--section__subsection--button">Search</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
  import autocomplete from "../components/autocomplete";
  import search from "../components/search";

  export default {
    components: {
      autocomplete,
      search
    },
    data() {
      return {
        location: '',
        selected_location: '',
        find_locations: []
      }
    },
    head() {
      return {
        title: 'wodeveryday',
        meta: [
          // hid is used as unique identifier. Do not use `vmid` for it as it will not work
          // {
          //   hid: 'description',
          //   name: 'description',
          //   content: 'My custom description'
          // }
        ]
      }
    },
    methods: {
      searchLocation(data) {
        this.$store.dispatch('searchLocation', {search_text: data}).then(response => {
          this.find_locations = response
        })
      },
      pushContinent(continent) {
        this.$router.push("find/" + continent + '/')
      }
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
