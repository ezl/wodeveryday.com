<template>
  <search-card
    :is-loading="isLoading"
    :item-list="cityList"
    :select-item="selectCity"
    :custom-back-button-enabled="true"
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
      itemTitle: "City",
      cityList: [],
      isLoading: true,
    }
  },
  mounted() {
    this.fetchCities()
  },
  methods: {
    fetchCities() {
      this.isLoading = true
      let url = `${process.env.BACKEND_URL}/affiliates/cities/`
      let currentState = this.$store.state.current_state
      if (currentState === "none") {
        url += `?country=${this.$store.state.current_country}`
      } else {
        url += `?state=${currentState}`
      }
      url = encodeURI(url)
      let that = this
      this.$axios
        .$get(url)
        .then((response) => {
          that.cityList = response.cities
          that.$store.commit("SET_CITIES", that.cityList)
          that.isLoading = false
        })
        .catch(function (error) {
          console.log(error)
          that.isLoading = false
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
    selectCity(cityName) {
      this.$store.commit("SET_CURRENT_CITY", cityName)
      this.$router.push(`${cityName}/`)
    },
  },
}
</script>
