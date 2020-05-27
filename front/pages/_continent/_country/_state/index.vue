<template>
  <search-card
    :item-list="cityList"
    :select-item="selectCity"
    :select-subitem="selectGym"
    :item-title="itemTitle"
  />
</template>

<script>
import SearchCard from "~/components/navigation/SearchCard.vue"

export default {
  components: {
    SearchCard,
  },
  data() {
    return {
      itemTitle: "state",
      cityList: {},
    }
  },
  mounted() {
    this.$retrievePathVariables(this.$store, this.$route.params)
    this.fetchCities()
    this.$generateBreadcrumb(this.$store, this.$route.params, this.itemTitle)
  },
  methods: {
    fetchCitiesURL() {
      let url = `${process.env.BACKEND_URL}/affiliates/gyms/`
      const state = this.$store.state[`current_${this.itemTitle}`]
      if (state === this.$store.state.constants.NOSTATE) {
        this.itemTitle = "country"
        const country = this.$store.state[`current_${this.itemTitle}`]
        url += `?country=${country}`
      } else {
        url += `?state=${state}`
      }
      url = encodeURI(url)
      return url
    },
    fetchCities() {
      const url = this.fetchCitiesURL()
      let that = this
      this.$axios
        .$get(url)
        .then((response) => {
          that.cityList = response
          that.$store.commit("SET_CITIES", that.cityList)
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    fetchGym(cityName, gymName) {
      const url = `${process.env.BACKEND_URL}/affiliates/?city__iexact=${cityName}&name__iexact=${gymName}`
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
    selectCity(cityName) {
      this.$store.commit("SET_CURRENT_CITY", cityName)
      this.$pushCleanedRoute(this.$router, `${cityName}/`)
    },
    selectGym(gymName) {
      let cityName = this.$findParent(this.cityList, gymName)
      this.$store.commit("SET_CURRENT_CITY", cityName)
      this.fetchGym(cityName, gymName)
    },
    navigateToGym(cityName, gymName) {
      this.$pushCleanedRoute(this.$router, `${cityName}/${gymName}/`)
    },
  },
}
</script>
