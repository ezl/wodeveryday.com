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

export default {
  components: {
    GeographySearchPage,
  },
  data() {
    return {
      itemTitle: "continent",
    }
  },
  computed: {
    fetchCountriesURL: function () {
      const continent = this.$store.state[`current_${this.itemTitle}`]
      let url = `${process.env.BACKEND_URL}/affiliates/countries/?continent=${continent}`
      url = encodeURI(url)
      return url
    },
    fetchPageTitle: function () {
      return this.$store.state.constants.GEO_PAGE_TITLE.replace(
        "{}",
        this.$store.state[`current_${this.itemTitle}`]
      )
    },
  },
  mounted() {
    this.$retrievePathVariables(this.$store, this.$route.params)
    this.fetchCountries()
    this.$generateBreadcrumb(this.$store, this.$route.params, this.itemTitle)
  },
  methods: {
    fetchCountries() {
      const url = this.fetchCountriesURL
      apiLibrary.retrieveCountries(url, this.$store)
    },
    selectCountry(countryName) {
      this.$store.commit("SET_CURRENT_COUNTRY", countryName)
      if (
        this.$store.state.constants.COUNTRIES_WITH_STATES.includes(
          this.$store.state.current_country
        )
      ) {
        this.$pushCleanedRoute(this.$router, `${countryName}/`)
      } else {
        this.$store.commit(
          "SET_CURRENT_STATE",
          this.$store.state.constants.NOSTATE
        )
        this.$pushCleanedRoute(
          this.$router,
          `${countryName}/${this.$store.state.constants.NOSTATE}/`
        )
      }
    },
    selectCityOrState(cityOrStateName) {
      const countryName = this.$findParent(
        this.$store.state.countries,
        cityOrStateName
      )
      this.$store.commit("SET_CURRENT_COUNTRY", countryName)
      if (
        this.$store.state.constants.COUNTRIES_WITH_STATES.includes(
          this.$store.state.current_country
        )
      ) {
        this.$store.commit("SET_CURRENT_STATE", cityOrStateName)
        this.$pushCleanedRoute(
          this.$router,
          `${countryName}/${cityOrStateName}/`
        )
      } else {
        this.$store.commit("SET_CURRENT_CITY", cityOrStateName)
        this.$pushCleanedRoute(
          this.$router,
          `${countryName}/${this.$store.state.constants.NOSTATE}/${cityOrStateName}/`
        )
      }
    },
  },
  head() {
    return {
      title: this.fetchPageTitle,
      meta: [
        {
          property: "og:title",
          content: this.fetchPageTitle,
        },
        {
          property: "og:description",
          content: this.$store.state.constants.DEFAULT_META_DESCRIPTION,
        },
        {
          property: "og:image",
          content: this.$store.state.constants.DEFAULT_GYM_THUMBNAIL,
        },
      ],
    }
  },
}
</script>
