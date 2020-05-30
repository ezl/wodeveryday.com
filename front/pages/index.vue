<template>
  <search-card
    :item-list="$store.state.continents"
    :select-item="selectContinent"
    :select-subitem="selectCountry"
  />
</template>

<script>
import SearchCard from "~/components/navigation/SearchCard.vue"
import actions from "~/store/actions.js"

export default {
  components: {
    SearchCard,
  },
  computed: {
    fetchContinentURL: function () {
      let url = `${process.env.BACKEND_URL}/affiliates/continents`
      url = encodeURI(url)
      return url
    },
  },
  mounted() {
    // ToDo: remove this line when the routing structure is improved.
    // It is a temporary fix that resolves an issue where navigating to a state
    // country after navigating to a nostate country isn't possible due to the
    // convoluted routing structure
    this.$store.commit("RESET_STATE")

    this.fetchContinents()
    this.$generateBreadcrumb(this.$store, this.$route.params)
  },
  methods: {
    fetchContinents() {
      const url = this.fetchContinentURL
      actions.retrieveContinents(url, this.$store)
    },
    selectContinent(continentName) {
      this.$store.commit("SET_CURRENT_CONTINENT", continentName)
      this.$pushCleanedRoute(this.$router, `${continentName}/`)
    },
    selectCountry(countryName) {
      const continentName = this.$findParent(
        this.$store.state.continents,
        countryName
      )
      this.$store.commit("SET_CURRENT_CONTINENT", continentName)
      this.$store.commit("SET_CURRENT_COUNTRY", countryName)
      if (
        this.$store.state.constants.COUNTRIES_WITH_STATES.includes(
          this.$store.state.current_country
        )
      ) {
        this.$pushCleanedRoute(this.$router, `${continentName}/${countryName}/`)
      } else {
        this.$store.commit(
          "SET_CURRENT_STATE",
          this.$store.state.constants.NOSTATE
        )
        this.$pushCleanedRoute(
          this.$router,
          `${continentName}/${countryName}/${this.$store.state.constants.NOSTATE}/`
        )
      }
    },
  },
}
</script>
