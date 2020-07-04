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
import reusableFunctionsLibrary from "~/store/reusableFunctionsLibrary.js"

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
      reusableFunctionsLibrary.pushCleanedRoute(this.$router, `${stateName}/`)
    },
    selectCity(stateName, cityName) {
      reusableFunctionsLibrary.pushCleanedRoute(
        this.$router,
        `${stateName}/${cityName}/`
      )
    },
  },
}
</script>
