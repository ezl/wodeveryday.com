<template>
  <search-card
    :item-list="$store.state.countries"
    :select-item="selectCountry"
    :select-subitem="selectCityOrState"
    :item-title="itemTitle"
  />
</template>

<script>
import SearchCard from "~/components/navigation/SearchCard.vue"
import actions from "~/store/actions.js"

export default {
  components: {
    SearchCard,
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
  },
  mounted() {
    this.$retrievePathVariables(this.$store, this.$route.params)
    this.fetchCountries()
    this.$generateBreadcrumb(this.$store, this.$route.params, this.itemTitle)
  },
  methods: {
    fetchCountries() {
      const url = this.fetchCountriesURL
      actions.retrieveCountries(url, this.$store)
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
}
</script>
