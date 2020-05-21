<template>
  <gym-search-card
    :is-loading="isLoading"
    :gym-list="affiliateList"
    :select-item="selectAffiliate"
    :item-title="itemTitle"
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
      itemTitle: "city",
      affiliateList: [],
      isLoading: false,
    }
  },
  mounted() {
    this.fetchAffiliates()
    this.$generateBreadcrumb(this.$store, this.itemTitle)
  },
  methods: {
    fetchAffiliates() {
      const country = this.$retrieveStoredPathVariable(
        "country",
        this.$store,
        this.$route.params
      )
      const state = this.$retrieveStoredPathVariable(
        "state",
        this.$store,
        this.$route.params
      )
      const city = this.$retrieveStoredPathVariable(
        "city",
        this.$store,
        this.$route.params
      )
      let url = `${process.env.BACKEND_URL}/affiliates/?city=${city}&country=${country}`
      if (state != this.$store.state.constants.NOSTATE) url += `&state=${state}`
      url = encodeURI(url)
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
    selectAffiliate(selectedAffiliate) {
      this.$store.commit("SET_CURRENT_AFFILIATE", selectedAffiliate)
      this.$router.push(`${selectedAffiliate.name}/`)
    },
  },
}
</script>
