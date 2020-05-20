<template>
  <search-card
    :is-loading="isLoading"
    :item-list="cityList"
    :select-item="selectCity"
    :select-subitem="selectGym"
    :item-title="itemTitle"
    :card-title="cardTitle"
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
      cardTitle: undefined,
      itemTitle: undefined,
      cityList: {},
      isLoading: true,
    }
  },
  mounted() {
    this.fetchCities()
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
    fetchCities() {
      this.isLoading = true
      let url = `${process.env.BACKEND_URL}/affiliates/gyms/`
      const state = this.retrieveStoredPathVariable("state")
      if (state === "none") {
        const country = this.retrieveStoredPathVariable("country")
        url += `?country=${country}`
        this.itemTitle = "country"
      } else {
        url += `?state=${state}`
        this.itemTitle = "state"
      }
      url = encodeURI(url)
      let that = this
      this.$axios
        .$get(url)
        .then((response) => {
          that.cityList = response
          that.$store.commit("SET_CITIES", that.cityList)
          that.isLoading = false
        })
        .catch(function (error) {
          console.log(error)
          that.isLoading = false
        })
    },
    fetchGym(cityName, gymName) {
      let url = `${process.env.BACKEND_URL}/affiliates/?city=${cityName}&name=${gymName}`
      let that = this
      this.$axios
        .$get(url)
        .then((response) => {
          const selectedAffiliate = response.results[0]
          that.$store.commit("SET_CURRENT_AFFILIATE", selectedAffiliate)
          that.navigateToGym(cityName, gymName)
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    getStateOrCountry() {
      let currentState = this.$store.state.current_state
      if (currentState) {
        return `${this.$store.state.current_country}/${currentState}`
      } else {
        return ``
      }
    },
    findParent(registryObject, name) {
      registryObject = Object.entries(registryObject)
      let parentName = registryObject.find(
        (parent) => parent[1].indexOf(name) !== -1
      )
      return parentName[0]
    },
    selectCity(cityName) {
      this.$store.commit("SET_CURRENT_CITY", cityName)
      this.$router.push(`${cityName}/`)
    },
    selectGym(gymName) {
      let cityName = this.findParent(this.cityList, gymName)
      this.$store.commit("SET_CURRENT_CITY", gymName)
      this.fetchGym(cityName, gymName)
    },
    navigateToGym(cityName, gymName) {
      this.$router.push(`${cityName}/${gymName}/`)
    },
  },
}
</script>
