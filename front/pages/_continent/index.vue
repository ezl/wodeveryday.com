<template>
  <search-card
    :is-loading="isLoading"
    :item-list="countryList"
    :select-item="selectCountry"
    :select-subitem="selectCityOrState"
    :back-button-enabled="true"
    :item-title="itemTitle"
  />
</template>

<script>
import SearchCard from "~/components/SearchCard.vue"

export default {
  components: {
    SearchCard,
  },
  data() {
    return {
      itemTitle: "continent",
      countryList: {},
      isLoading: true,
    }
  },
  mounted() {
    this.fetchCountries()
    this.generateBreadcrumb()
  },
  methods: {
    generateBreadcrumb() {
      let pages = ["continent", "country", "state", "gym"]
      let currentPage = pages.indexOf(this.itemTitle || "")
      if (currentPage != -1) {
        let breadcrumbNames = ["Home"]
        for (let i = 0; i <= currentPage; i++) {
          let name = this.$store.state["current_" + pages[i]]
          if (name != "none") breadcrumbNames.push(name)
        }
        this.$store.commit("SET_GLOBAL_BREADCRUMB_NAMES", breadcrumbNames)
      } else {
        this.$store.commit("SET_GLOBAL_BREADCRUMB_NAMES", [])
      }
    },
    retrieveStoredPathVariable(pathVarName) {
      let pathVariable = this.$store.state[`current_${pathVarName}`]
      if (pathVariable === undefined) {
        pathVariable = this.$route.params[pathVarName]
        this.$store.commit(
          `SET_CURRENT_${pathVarName.toUpperCase()}`,
          pathVariable
        )
      }
      return pathVariable
    },
    fetchCountries() {
      const continent = this.retrieveStoredPathVariable("continent")
      this.isLoading = true
      let url = `${process.env.BACKEND_URL}/affiliates/countries/?continent=${continent}`
      url = encodeURI(url)
      let that = this
      this.$axios
        .$get(url)
        .then((response) => {
          that.countryList = response
          that.$store.commit("SET_COUNTRIES", that.countryList)
          that.isLoading = false
        })
        .catch(function (error) {
          console.log(error)
          that.isLoading = false
        })
    },
    selectCountry(countryName) {
      this.$store.commit("SET_CURRENT_COUNTRY", countryName)
      if (
        ["United States", "Australia", "Canada"].includes(
          this.$store.state.current_country
        )
      ) {
        this.$router.push(`${countryName}/`)
      } else {
        this.$store.commit("SET_CURRENT_STATE", "none")
        this.$router.push(`${countryName}/none/`)
      }
    },
    findParent(registryObject, name) {
      registryObject = Object.entries(registryObject)
      let parentName = registryObject.find(
        (parent) => parent[1].indexOf(name) !== -1
      )
      return parentName[0]
    },
    selectCityOrState(cityOrStateName) {
      let countryName = this.findParent(this.countryList, cityOrStateName)
      this.$store.commit("SET_CURRENT_COUNTRY", countryName)
      if (
        ["United States", "Australia", "Canada"].includes(
          this.$store.state.current_country
        )
      ) {
        this.$store.commit("SET_CURRENT_STATE", cityOrStateName)
        this.$router.push(`${countryName}/${cityOrStateName}/`)
      } else {
        this.$store.commit("SET_CURRENT_CITY", cityOrStateName)
        this.$router.push(`${countryName}/none/${cityOrStateName}/`)
      }
    },
  },
}
</script>
