<template>
  <geography-search-page
    :item-list="$store.state.countries"
    :select-item="selectCountry"
    :select-subitem="selectCityOrState"
    :item-title="itemTitle"
  />
</template>

<script>
import GeographySearchPage from "~/components/navigation/GeographySearchPage.vue"
import apiLibrary from "~/store/apiLibrary.js"
import _ from "lodash"
import reusableFunctionsLibrary from "~/store/reusableFunctionsLibrary.js"

export default {
  components: {
    GeographySearchPage,
  },
  async asyncData({ store, route }) {
    const continent = _.capitalize(route.params["continent"]).replace(
      /-/gi,
      " "
    )
    const url = `${process.env.BACKEND_URL}/gyms/countries/?continent=${continent}`
    await apiLibrary.retrieveCountries(url, store)

    const pageTitle = store.state.constants.GEO_PAGE_TITLE.replace(
      "{}",
      continent
    )
    let metaTags = reusableFunctionsLibrary.generateMetaTags(
      store,
      pageTitle,
      store.state.constants.DEFAULT_META_DESCRIPTION,
      store.state.constants.DEFAULT_GYM_THUMBNAIL,
      route.fullPath
    )
    return {
      metaTags: metaTags,
      pageTitle: pageTitle,
    }
  },
  data() {
    return {
      itemTitle: "continent",
      metaTags: [],
      pageTitle: "",
    }
  },
  methods: {
    selectCountry(countryName) {
      reusableFunctionsLibrary.pushCleanedRoute(this.$router, `${countryName}/`)
    },
    selectCityOrState(countryName, cityOrStateName) {
      reusableFunctionsLibrary.pushCleanedRoute(
        this.$router,
        `${countryName}/${cityOrStateName}/`
      )
    },
  },
  head() {
    return {
      title: this.pageTitle,
      meta: this.metaTags,
    }
  },
}
</script>
