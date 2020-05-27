<template>
  <gym-search-card
    :gym-list="affiliateList"
    :select-item="selectAffiliate"
    :item-title="itemTitle"
  />
</template>

<script>
import GymSearchCard from "~/components/navigation/GymSearchCard.vue"

export default {
  components: {
    GymSearchCard,
  },
  data() {
    return {
      itemTitle: "city",
      affiliateList: [],
    }
  },
  computed: {
    fetchGymsURL: () => {
      const country = this.$store.state["current_country"]
      const state = this.$store.state["current_state"]
      const city = this.$store.state[`current_${this.itemTitle}`]
      let url = `${process.env.BACKEND_URL}/affiliates/?city__iexact=${city}&country__iexact=${country}`
      if (state != this.$store.state.constants.NOSTATE)
        url += `&full_state__iexact=${state}`
      url = encodeURI(url)
      return url
    },
  },
  mounted() {
    this.$retrievePathVariables(this.$store, this.$route.params)
    this.fetchAffiliates()
    this.$generateBreadcrumb(this.$store, this.$route.params, this.itemTitle)
  },
  methods: {
    fetchAffiliates() {
      const url = this.fetchGymsURL
      let that = this
      this.$axios
        .$get(url)
        .then((response) => {
          that.affiliateList = response.results
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    selectAffiliate(selectedAffiliate) {
      this.$store.commit("SET_CURRENT_AFFILIATE", selectedAffiliate)
      this.$pushCleanedRoute(this.$router, `${selectedAffiliate.name}/`)
    },
  },
}
</script>
