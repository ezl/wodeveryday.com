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
  asyncData({ store, route }) {
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
  computed: {
    fetchContinentURL: function () {
      const url = `${process.env.BACKEND_URL}/affiliates/continents`
      return url
    },
  },
  mounted() {
    this.fetchContinents()
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
