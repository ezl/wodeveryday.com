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

export default {
  components: {
    GeographySearchPage,
  },
  data() {
    return {
      itemTitle: "continent",
      metaTags: [],
    }
  },
  computed: {
    fetchCountriesURL: function () {
      const continent = this.$route.params[this.itemTitle].replace(/-/gi, " ")
      const url = `${process.env.BACKEND_URL}/affiliates/countries/?continent=${continent}`
      return url
    },
    fetchPageTitle: function () {
      return this.$store.state.constants.GEO_PAGE_TITLE.replace(
        "{}",
        _.capitalize(this.$route.params[this.itemTitle]).replace(/-/gi, " ")
      )
    },
  },
  mounted() {
    this.fetchCountries()
    this.metaTags = this.$generateMetaTags(
      this.$store,
      this.fetchPageTitle,
      this.$store.state.constants.DEFAULT_META_DESCRIPTION,
      this.$store.state.constants.DEFAULT_GYM_THUMBNAIL
    )
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
      title: this.fetchPageTitle,
      meta: this.metaTags,
    }
  },
}
</script>
