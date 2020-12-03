<template>
  <header class="header">
    <b-navbar toggleable="lg" type="dark" variant="dark" class="p-lg-0 header__custom--navbar">
      <div class="container align-items-lg-end">
        <b-navbar-brand href="#">
          <img src="~/assets/img/logo2.svg" alt="" width="150">
        </b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <li class="nav-item">
              <router-link class="nav-link" exact-active-class="active nav-link" :to="{name:'index'}">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" exact-active-class="active nav-link" :to="{name:'about'}">About us
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" exact-active-class="active nav-link" :to="{name:'blog'}">Blog</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" exact-active-class="active nav-link" :to="{name:'contact'}">Contact
              </router-link>
            </li>
          </b-navbar-nav>
          <div class="header__curtom_search" :class="search ? 'active': ''">
            <font-awesome-icon :icon="['fas', 'search']" @click="searchshow" class="header__curtom_search--icon"/>
            <div class="header__curtom_search--dropdown" v-if="search">
              <div class="position-relative">
                <label class="m-0">
                  <span class="screen-reader-text">Search for:</span>
                  <input type="search" class="search-field" placeholder="Search …" value="" name="s">
                </label>
                <button type="submit" class="search-submit">
                  <font-awesome-icon :icon="['fas', 'search']"/>
                </button>
              </div>

            </div>
          </div>
        </b-collapse>
      </div>
    </b-navbar>
  </header>
</template>

<script>
  export default {
    data() {
      return {
        search: false
      }
    },
    methods: {
      searchshow() {
        return this.search = !this.search
      }
    }
  }
</script>

<style lang="scss" scoped>
  .header {
    border-top: 15px solid var(--brand-color);
    border-bottom: 5px solid var(--brand-color);

    &__custom--navbar {
      .navbar-nav {
        margin-bottom: -1px;
      }

      .nav-link {
        padding: 5px 15px !important;
        text-transform: uppercase;
        font-weight: 400;
        transition: all 0.2s ease;

        &:hover,
        &:focus {
          background: var(--brand-color);
          color: var(--brand-color-two) !important;
        }
      }
    }

    &__curtom_search {
      position: relative;
      padding: 5px 10px;

      .nav-link {
        color: var(--brand-color) !important;
      }

      &--dropdown {
        position: absolute;
        width: 250px;
        right: 0;
        top: 115%;
        padding: 10px;
        background: var(--brand-color);

      }

      @media screen and (max-width: 991px) {
        &--dropdown {
          left: 0;
          right: auto;
          top: 130%;
          width: 100%;
        }
      }

      &--icon {
        color: var(--brand-color);
        cursor: pointer;
      }
    }

    .active .nav-link {
      background: var(--brand-color);
      color: var(--brand-color-two) !important;
    }
  }

  .screen-reader-text {
    clip: rect(1px, 1px, 1px, 1px);
    position: absolute !important;
    white-space: nowrap;
    height: 0;
    width: 1px;
    overflow: hidden;
  }

  .search-field {
    background: #fff;
    border: 1px solid #ccc;
    color: #000;
    width: 100%;
    float: left;
    font-size: 16px;
    padding: 0 15px;
    height: 40px;
    line-height: 48px;
    outline: none;
    -webkit-border-radius: 0;
    -moz-border-radius: 0;
    border-radius: 0;
    transition: all 0.5s ease-in-out;
    transition: all 0.5s ease-in-out;
    -moz-transition: all 0.5s ease-in-out;
    -ms-transition: all 0.5s ease-in-out;
    -o-transition: all 0.5s ease-in-out;
    -webkit-transition: all 0.5s ease-in-out;
  }

  .search-submit {
    background: var(--brand-color-two);
    border: none;
    padding: 0;
    position: absolute;
    text-align: center;
    color: #fff;
    line-height: 40px;
    height: 40px;
    width: 51px;
    top: 0;
    right: 0;
    transition: all 0.5s ease-in-out;
    transition: all 0.5s ease-in-out;
    -moz-transition: all 0.5s ease-in-out;
    -ms-transition: all 0.5s ease-in-out;
    -o-transition: all 0.5s ease-in-out;
    -webkit-transition: all 0.5s ease-in-out;
  }

  @media screen and (max-width: 600px) {
    .header {
      img {
        width: 100px !important;
      }
    }
  }
</style>
