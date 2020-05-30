<template>
  <v-card id="leaderboard" class="mb-3">
    <v-card-text v-if="!leaderboardItems" class="text-center">
      <v-progress-circular :size="70" :width="7" color="white" indeterminate />
    </v-card-text>
    <template v-if="leaderboardItems && leaderboardItems.length > 0">
      <v-card-text>
        <h3>Crossfit Games Participants</h3>
      </v-card-text>

      <v-data-table
        :headers="leaderboardHeaders"
        :items="leaderboardItems"
        :options.sync="options"
        disable-sort
        :footer-props="{
          'items-per-page-options': [50],
          'items-per-page-text': null,
        }"
        :server-items-length="leaderboardTotalItems"
        :loading="tableLoading"
        class="elevation-1"
      />
    </template>
  </v-card>
</template>

<script>
import apiLibrary from "~/store/apiLibrary.js"

export default {
  name: "LeaderboardCard",
  data() {
    return {
      leaderboardData: [],
      leaderboardTotalItems: 0,
      leaderboardItems: undefined,
      leaderboardHeaders: [
        { text: "RANK", value: "rank" },
        { text: "NAME", value: "name" },
        { text: "POINTS", value: "points" },
        { text: "20.1", value: "20.1" },
        { text: "20.2", value: "20.2" },
        { text: "20.3", value: "20.3" },
        { text: "20.4", value: "20.4" },
        { text: "20.5", value: "20.5" },
      ],
      rankSuffix: ["", "st", "nd", "rd", "th"],
      leaderboardPage: 1,
      options: { page: 1 },
      tableLoading: true,
    }
  },
  computed: {
    gymName: function () {
      return this.$store.state.gym_object.name
    },
  },
  watch: {
    options: {
      handler(oldVal, newVal) {
        if (oldVal.page === newVal.page) return
        this.fetchLeaderboardData()
      },
      deep: true,
    },
  },
  mounted() {
    this.fetchLeaderboardData()
  },
  methods: {
    fetchLeaderboardData() {
      const url = `${process.env.BACKEND_URL}/affiliate_leaderboard/`
      const parameters = {
        affiliate_name: this.$store.state.gym_object.name,
        page: this.options.page,
      }
      this.tableLoading = true
      apiLibrary
        .retrieveLeaderboardData(url, parameters)
        .then((data) => {
          this.leaderboardData = data
          if (data.pagination !== undefined)
            this.leaderboardTotalItems = data.pagination.totalCompetitors
          this.formatLeaderboardData()
          this.tableLoading = false
        })
        .catch(function (error) {
          console.log(error)
          this.leaderboardData = []
          this.leaderboardItems = []
          this.tableLoading = false
        })
    },
    formatLeaderboardData() {
      this.leaderboardItems = []
      if (this.leaderboardData.leaderboardRows === undefined) return

      if (this.$store.state["gymNavbarOptions"].indexOf("Leaderboard") === -1) {
        this.$store.commit("PUSH_TO_GYM_NAVBAR_OPTIONS", "Leaderboard")
        this.$store.commit("PUSH_TO_GYM_NAVBAR_GOTO_ELEMENTS", "#leaderboard")
      }

      const leaderboardRows = this.leaderboardData.leaderboardRows
      leaderboardRows.forEach((dataRow) => {
        this.leaderboardItems.push(this.createLeaderBoardItemObject(dataRow))
      })
    },
    createLeaderBoardItemObject(dataRow) {
      return {
        rank: dataRow.overallRank,
        name: dataRow.entrant.competitorName,
        points: dataRow.overallScore,
        "20.1": `${this.getRank(dataRow.scores[0].rank)} (${this.getScore(
          dataRow.scores[0].scoreDisplay
        )}`,
        "20.2": `${this.getRank(dataRow.scores[1].rank)} (${this.getScore(
          dataRow.scores[1].scoreDisplay
        )})`,
        "20.3": `${this.getRank(dataRow.scores[2].rank)} (${this.getScore(
          dataRow.scores[2].scoreDisplay
        )})`,
        "20.4": `${this.getRank(dataRow.scores[3].rank)} (${this.getScore(
          dataRow.scores[3].scoreDisplay
        )})`,
        "20.5": `${this.getRank(dataRow.scores[4].rank)} (${this.getScore(
          dataRow.scores[4].scoreDisplay
        )})`,
      }
    },
    getRank(rankNumber) {
      if (rankNumber > 3) {
        return rankNumber + "th"
      } else {
        return rankNumber + this.rankSuffix[rankNumber]
      }
    },
    getScore(scoreDisplay) {
      if (scoreDisplay.length > 0) {
        return scoreDisplay
      } else {
        return "--"
      }
    },
  },
}
</script>

<style lang="scss" scoped>
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}
::-webkit-scrollbar-track {
  background: transparent;
  border: 1px solid darkgray;
  border-radius: 5px;
}
::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
  background: #555;
  border-radius: 5px;
}
</style>
