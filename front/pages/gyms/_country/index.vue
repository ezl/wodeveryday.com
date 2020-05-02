<template>
  <search-card
    :is-loading="isLoading"
    :item-list="stateList"
    :select-item="selectState"
    :back-button-enabled="true"
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
      stateList: [],
      isLoading: true,
    }
  },
  mounted() {
    this.stateList = this.$store.state.states
    this.fetchStates()
  },
  methods: {
    fetchStates() {
      this.isLoading = true
      let url = `${process.env.BACKEND_URL}/affiliates/states/?country=${this.$store.state.current_country}`
      url = encodeURI(url)

      let that = this
      this.$axios
        .$get(url)
        .then((response) => {
          that.isLoading = false
          if (response.states.length > 0) {
            that.stateList = response.states
          } else {
            that.$store.commit("SET_CURRENT_STATE", "none")
            that.$router.push(`${that.$store.state.current_state}/`)
          }
        })
        .catch(function (error) {
          console.log(error)
          that.isLoading = false
        })
    },
    selectState(stateName) {
      this.$store.commit("SET_CURRENT_STATE", stateName)
      this.$router.push(`${stateName}/`)
    },
  },
}
</script>
