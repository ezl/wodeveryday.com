<template>
  <b-container fluid>
    <b-row class="w-100" align-h="center">
      <b-col :xl="2" :lg="4" :md="6" :sm="12" class="mb-4" v-for="(items,name) in items_object"
             :key="name">
        <b-card no-body bg-variant="dark" class="shadow">
          <template #header>
            <h5 class="mb-0">
              <router-link :to="formedLink(name)+'/'">{{name}}</router-link>
            </h5>
          </template>
          <b-list-group flush>
            <b-list-group-item class="list_item" v-for="(item,ind) in items"
                               :href="formedLink(name)+'/'+formedLink(item)+'/'"
                               :key="ind">
              {{formedItemTitle(item)}}
            </b-list-group-item>
          </b-list-group>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
  export default {
    name: "cards",
    props: {
      items_object: {
        type: Object,
        required: true
      }
    },
    methods: {
      formedItemTitle(str) {
        if (str === null || str === undefined)
          return str
        if (typeof str === 'string')
          return str
        else
          return this.formedItemTitle(str[0])
      },
      formedLink(str) {
        if (str === null || str === undefined)
          return '#'
        if (typeof str === 'string')
          return str.toLowerCase().replace(' ', '-')
        else
          return str[1]
      }
    }
  }
</script>

<style scoped>
  h5 {
    text-align: center;
  }

  .list_item {
    background-color: var(--brand-color);
    color: var(--brand-color-two);
    text-align: center;
  }

  .list_item:hover {
    background-color: var(--brand-color-two);
    color: var(--brand-color);
  }


  h5 a {
    color: var(--brand-color) !important;
  }

  h5 a:hover {
    text-decoration: none;
  }
</style>
