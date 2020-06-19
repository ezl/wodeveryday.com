<template>
  <v-card>
    <v-card-text v-if="!gymTimes" class="text-center">
      <v-progress-circular :size="70" :width="7" color="white" indeterminate />
    </v-card-text>
    <template v-if="gymTimes && gymTimes.length > 0">
      <v-card-text>
        <h3>Hours</h3>
      </v-card-text>
      <v-divider />
      <v-list>
        <v-list-item-group v-model="currentDayOfTheWeek">
          <v-list-item v-for="(time, index) in gymTimes" :key="index" disabled>
            <v-list-item-content>
              <v-list-item-title :key="index">
                {{ time }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </template>
  </v-card>
</template>

<script>
export default {
  name: "HoursCard",
  data() {
    return {
      currentDayOfTheWeek: this.getCurrentDayOfTheWeek(),
    }
  },
  computed: {
    gymTimes: function () {
      if (this.$store.state.place_details.opening_hours) {
        return this.$store.state.place_details.opening_hours.weekday_text || []
      }
      return []
    },
  },
  methods: {
    getCurrentDayOfTheWeek() {
      let currentDay = new Date().getDay()
      if (currentDay == 0) {
        this.currentDayOfTheWeek = 6
      } else {
        this.currentDayOfTheWeek = currentDay - 1
      }
      return this.currentDayOfTheWeek
    },
  },
}
</script>
