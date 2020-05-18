<template>
  <search-card
    :is-loading="isLoading"
    :item-list="stateList"
    :select-item="selectState"
    :select-subitem="selectCity"
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
      cardTitle: this.$store.state.current_country,
      itemTitle: "country",
      stateList: {},
      isLoading: true,
    }
  },
  mounted() {
    this.stateList = this.$store.state.states
    this.fetchStates()
  },
  methods: {
    fetchStates() {
      if (
        ["United States", "Australia", "Canada"].includes(
          this.$store.state.current_country
        )
      ) {
        this.isLoading = true
        let url = `${process.env.BACKEND_URL}/affiliates/states/?country=${this.$store.state.current_country}`
        url = encodeURI(url)

        let that = this
        this.$axios
          .$get(url)
          .then((response) => {
            that.isLoading = false
            that.stateList = response
          })
          .catch(function (error) {
            console.log(error)
            that.isLoading = false
          })
      } else {
        this.$store.commit("SET_CURRENT_STATE", "none")
        this.$router.push(`${this.$store.state.current_state}/`)
      }
    },
    selectState(stateName) {
      this.$store.commit("SET_CURRENT_STATE", stateName)
      this.$router.push(`${stateName}/`)
    },
    selectCity(cityName) {
      this.$store.commit("SET_CURRENT_CITY", cityName)
      this.$router.push(`${cityName}/`)
    },
  },
}
</script>
