<template>
  <search-card
    :is-loading="isLoading"
    :item-list="countryList"
    :select-item="selectCountry"
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
      countryList: [],
      isLoading: true,
    }
  },
  mounted() {
    this.fetchCountries()
  },
  methods: {
    fetchCountries() {
      this.isLoading = true
      let url = `${process.env.BACKEND_URL}/affiliates/countries`
      url = encodeURI(url)
      let that = this
      this.$axios
        .$get(url)
        .then((response) => {
          that.countryList = response.countries
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
      this.$router.push(`${countryName}/`)
    },
  },
}
</script>
