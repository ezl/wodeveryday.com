<template>
  <search-card
    :is-loading="isLoading"
    :item-list="countryList"
    :select-item="selectCountry"
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
      itemTitle: "country",
      countryList: [],
      isLoading: true,
    }
  },
  mounted() {
    this.fetchCountries()
  },
  methods: {
    fetchCountries() {
      this.countryList = this.$store.state.countries
      if (this.countryList.length === 0) {
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
      } else {
        this.isLoading = false
      }
    },
    selectCountry(countryName) {
      this.$store.commit("SET_CURRENT_COUNTRY", countryName)
      this.$router.push(`${countryName}/`)
    },
  },
}
</script>
