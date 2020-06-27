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

export default {
  components: {
    GeographySearchPage,
  },
  data() {
    return {
      metaTags: [],
    }
  },
  computed: {
    fetchContinentURL: function () {
      let url = `${process.env.BACKEND_URL}/affiliates/continents`
      url = encodeURI(url)
      return url
    },
  },
  mounted() {
    this.fetchContinents()
    this.metaTags = this.$generateMetaTags(
      this.$store,
      this.$store.state.constants.HOME_PAGE_TITLE,
      this.$store.state.constants.DEFAULT_META_DESCRIPTION,
      this.$store.state.constants.DEFAULT_GYM_THUMBNAIL
    )
  },
  methods: {
    fetchContinents() {
      const url = this.fetchContinentURL
      apiLibrary.retrieveContinents(url, this.$store)
    },
    selectContinent(continentName) {
      this.$pushCleanedRoute(this.$router, `find/${continentName}/`)
    },
    selectCountry(continentName, countryName) {
      this.$pushCleanedRoute(
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
