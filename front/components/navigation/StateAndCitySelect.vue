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

export default {
  name: "StateAndCitySelect",
  components: {
    GeographySearchPage,
  },
  data() {
    return {
      itemTitle: "country",
    }
  },
  methods: {
    selectState(stateName) {
      this.$pushCleanedRoute(this.$router, `${stateName}/`)
    },
    selectCity(stateName, cityName) {
      this.$pushCleanedRoute(this.$router, `${stateName}/${cityName}/`)
    },
  },
}
</script>
