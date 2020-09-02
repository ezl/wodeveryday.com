<template>
  <geography-search-page
    :item-list="$store.state.continents"
    :select-item="selectContinent"
    :select-subitem="selectCountry"
  />
</template>

<script>
import GeographySearchPage from "~/components/navigation/GeographySearchPage.vue"
import apiLibrary from "~/store/apiLibrary.js"
import reusableFunctionsLibrary from "~/store/reusableFunctionsLibrary.js"

export default {
  components: {
    GeographySearchPage,
  },
  async asyncData({ store, route }) {
    const url = `${process.env.BACKEND_URL}/gyms/continents`
    await apiLibrary.retrieveContinents(url, store)

    let metaTags = reusableFunctionsLibrary.generateMetaTags(
      store,
      store.state.constants.HOME_PAGE_TITLE,
      store.state.constants.DEFAULT_META_DESCRIPTION,
      store.state.constants.DEFAULT_GYM_THUMBNAIL,
      route.fullPath
    )
    return {
      metaTags: metaTags,
    }
  },
  data() {
    return {
      metaTags: [],
    }
  },
  methods: {
    selectContinent(continentName) {
      reusableFunctionsLibrary.pushCleanedRoute(
        this.$router,
        `find/${continentName}/`
      )
    },
    selectCountry(continentName, countryName) {
      reusableFunctionsLibrary.pushCleanedRoute(
        this.$router,
        `find/${continentName}/${countryName}/`
      )
    },
  },
  head() {
    return {
      title: this.$store.state.constants.HOME_PAGE_TITLE,
      meta: this.metaTags,
    }
  },
}
</script>
