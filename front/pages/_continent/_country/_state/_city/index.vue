<template>
  <gym-search-card
    :is-loading="isLoading"
    :gym-list="affiliateList"
    :select-item="selectAffiliate"
    :item-key="'name'"
    :back-button-enabled="true"
    :item-title="itemTitle"
    :card-title="cardTitle"
  />
</template>

<script>
import GymSearchCard from "~/components/GymSearchCard.vue"

export default {
  components: {
    GymSearchCard,
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
      let url = `${process.env.BACKEND_URL}/affiliates/?city=${this.$store.state.current_city}`
      // let currentState = this.$store.state.current_state
      // if (currentState) {
      //   url += `&state=${currentState}`
      // }
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
