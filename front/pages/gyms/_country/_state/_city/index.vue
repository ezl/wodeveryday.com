<template>
  <search-card
    :is-loading="isLoading"
    :item-list="affiliateList"
    :select-item="selectAffiliate"
    :item-key="'name'"
    :back-button-enabled="true"
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
      cardTitle: this.$store.state.current_city,
      itemTitle: "gym",
      affiliateList: [],
      isLoading: false,
    }
  },
  mounted() {
    this.fetchAffiliates()
  },
  methods: {
    fetchAffiliates() {
      let url = `${process.env.BACKEND_URL}/affiliates/?country=${this.$store.state.current_country}&city=${this.$store.state.current_city}`
      let currentState = this.$store.state.current_state
      if (currentState) {
        url += `&state=${currentState}`
      }
      let that = this
      this.$axios
        .$get(url)
        .then((response) => {
          that.affiliateList = response.results
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
        return `${this.$store.state.current_country}/none`
      }
    },
    selectAffiliate(selectedAffiliate) {
      this.$store.commit("SET_CURRENT_AFFILIATE", selectedAffiliate)
      this.$router.push(`${selectedAffiliate.name}/`)
    },
  },
}
</script>
