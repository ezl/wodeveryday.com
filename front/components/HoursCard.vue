<template>
  <v-card class="mb-3">
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
  props: {
    gymTimes: {
      type: Array,
      required: false,
      default: undefined,
    },
    gymName: {
      type: String,
      required: false,
      default: undefined,
    },
    currentDayOfTheWeek: {
      type: Number,
      required: false,
      default: 0,
    },
  },
}
</script>
