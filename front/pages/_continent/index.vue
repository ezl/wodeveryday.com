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
  },
  methods: {
    fetchCountries() {
      this.countryList = this.$store.state.countries
      if (Object.values(this.countryList).length === 0) {
        this.isLoading = true
        let url = `${process.env.BACKEND_URL}/affiliates/countries/?continent=${this.$store.state.current_continent}`
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
      } else {
        this.isLoading = false
      }
    },
    selectCountry(countryName) {
      this.$store.commit("SET_CURRENT_COUNTRY", countryName)
      this.$router.push(`${countryName}/`)
    },
    selectCityOrState(countryName, cityOrStateName) {
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
