<template>
  <search-card
    :is-loading="isLoading"
    :item-list="cityList"
    :select-item="selectCity"
    :select-subitem="selectGym"
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
      itemTitle: undefined,
      cityList: {},
      isLoading: true,
    }
  },
  mounted() {
    this.fetchCities()
    this.$generateBreadcrumb(this.$store, this.itemTitle)
  },
  methods: {
    fetchCities() {
      this.isLoading = true
      let url = `${process.env.BACKEND_URL}/affiliates/gyms/`
      const state = this.$retrieveStoredPathVariable(
        "state",
        this.$store,
        this.$route.params
      )
      if (state === "none") {
        const country = this.$retrieveStoredPathVariable(
          "country",
          this.$store,
          this.$route.params
        )
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
    selectCity(cityName) {
      this.$store.commit("SET_CURRENT_CITY", cityName)
      this.$router.push(`${cityName}/`)
    },
    selectGym(gymName) {
      let cityName = this.$findParent(this.cityList, gymName)
      this.$store.commit("SET_CURRENT_CITY", gymName)
      this.fetchGym(cityName, gymName)
    },
    navigateToGym(cityName, gymName) {
      this.$router.push(`${cityName}/${gymName}/`)
    },
  },
}
</script>
