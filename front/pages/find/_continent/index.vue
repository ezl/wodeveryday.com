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
  asyncData({ store, route }) {
    const pageTitle = store.state.constants.GEO_PAGE_TITLE.replace(
      "{}",
      _.capitalize(route.params["continent"]).replace(/-/gi, " ")
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
  computed: {
    fetchCountriesURL: function () {
      const continent = this.$route.params[this.itemTitle].replace(/-/gi, " ")
      const url = `${process.env.BACKEND_URL}/gyms/countries/?continent=${continent}`
      return url
    },
  },
  mounted() {
    this.fetchCountries()
  },
  methods: {
    fetchCountries() {
      const url = this.fetchCountriesURL
      apiLibrary.retrieveCountries(url, this.$store)
    },
    selectCountry(countryName) {
      this.$pushCleanedRoute(this.$router, `${countryName}/`)
    },
    selectCityOrState(countryName, cityOrStateName) {
      this.$pushCleanedRoute(this.$router, `${countryName}/${cityOrStateName}/`)
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
