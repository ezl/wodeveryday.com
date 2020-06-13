<template>
  <geography-search-page
    :item-list="$store.state.states"
    :select-item="selectState"
    :select-subitem="selectCity"
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
      itemTitle: "country",
    }
  },
  computed: {
    fetchStatesURL: function () {
      const country = this.$store.state[`current_${this.itemTitle}`]
      let url = `${process.env.BACKEND_URL}/affiliates/states/?country=${country}`
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
    this.determineIfCountryHasStates()
    this.$retrievePathVariables(this.$store, this.$route.params)
    this.fetchStates()
    this.$generateBreadcrumb(this.$store, this.$route.params, this.itemTitle)
  },
  methods: {
    determineIfCountryHasStates() {
      if (
        this.$store.state.current_state === this.$store.state.constants.NOSTATE
      ) {
        this.$router.go(-1)
      } else if (
        !this.$store.state.constants.COUNTRIES_WITH_STATES.includes(
          this.$store.state.current_country
        )
      ) {
        this.$store.commit(
          "SET_CURRENT_STATE",
          this.$store.state.constants.NOSTATE
        )
        this.$pushCleanedRoute(
          this.$router,
          `${this.$store.state.current_state}/`
        )
      }
    },
    fetchStates() {
      const url = this.fetchStatesURL
      apiLibrary.retrieveStates(url, this.$store)
    },
    selectState(stateName) {
      this.$store.commit("SET_CURRENT_STATE", stateName)
      this.$pushCleanedRoute(this.$router, `${stateName}/`)
    },
    selectCity(cityName) {
      const stateName = this.$findParent(this.$store.state.states, cityName)
      this.$store.commit("SET_CURRENT_STATE", stateName)
      this.$store.commit("SET_CURRENT_CITY", cityName)
      this.$pushCleanedRoute(this.$router, `${stateName}/${cityName}/`)
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
