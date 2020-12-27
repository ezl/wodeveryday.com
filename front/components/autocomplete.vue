<template>
  <div>
    <div style="position: relative" :class="{'show':openSuggestion,'dropdown':true}">
      <input type="text" class="form-control autocomplete" v-model="value" placeholder="Search for a GYM or location"
             @keydown.enter="enter"
             @keydown.up="up"
             @keydown.down="down"
             @keyup="$emit('search', value)"
             @input="change">
      <button type="submit" class="search-submit" @click="suggestionClick(current)">
        <font-awesome-icon :icon="['fas', 'search']" class="banner__input--icon"/>
      </button>
      <ul :class="{'dropdown-menu':true,'items_list':true,'show':openSuggestion}"
          style="width: 100%;max-height: 35em;overflow-y: scroll">
        <li v-for="(suggestion,index) in suggestions" :class="{'active':isActive(index),'dropdown-item':true}"
            @click="suggestionClick(index)">
          <b-row>
            <b-col xl="9">
              {{suggestion.location_name}}
            </b-col>
            <b-col xl="3">
              <b-button class="items" style="width: 100%">
                {{suggestion.location_type}}
              </b-button>
            </b-col>
          </b-row>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
  export default {
    name: "autocomplete",
    data() {
      return {
        open: false,
        value: '',
        current: 0
      }
    },
    methods: {
      enter() {
        this.value = this.suggestions[this.current].location_name
        this.open = false
      },

      down() {
        if (this.current < this.suggestions.length - 1)
          this.current++
      },
      up() {
        if (this.current > 0)
          this.current--
      },
      isActive(index) {
        return index === this.current
      },
      suggestionClick(index) {
        this.value = this.suggestions[index].location_name
        this.$router.push('/' + this.suggestions[index].location_path + '/')
        this.open = false
      },
      change() {
        if (!this.open) {
          this.open = true
          this.current = 0
        }
      },
    },
    computed: {
      openSuggestion() {
        return this.value !== '' &&
          this.suggestions.length !== 0 &&
          this.open
      },
    },
    props: {
      suggestions: {
        type: Array,
        required: true
      },
      // value: {
      //   type: String,
      //   required: true
      // }
    }
  }
</script>

<style scoped>
  input {
    height: 44px;
    border-radius: 5px;
  }

  .active {
    background-color: var(--brand-color);
    color: var(--brand-color-two);
  }

  .active button.items {
    background-color: var(--brand-color-two);
    color: var(--brand-color);
  }

  button.items {
    background: var(--brand-color);
    color: var(--brand-color-two);
    border: none;
  }

  button.search-submit {
    background: var(--brand-color);
    border: none;
    padding: 0;
    position: absolute;
    text-align: center;
    color: #fff;
    line-height: 44px;
    height: 44px;
    width: 65px;
    top: 0;
    right: 0;
    transition: all 0.2s ease-in-out;
    border-radius: 0 5px 5px 0;
  }

  .items_list::-webkit-scrollbar {
    width: .5em;
  }

  .items_list::-webkit-scrollbar-track {
    /*box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);*/
    background-color: white;
  }

  .items_list::-webkit-scrollbar-thumb {
    background-color: var(--brand-color);
    outline: none;
    border-radius: 1em;
  }

  .autocomplete:focus {
    outline: none !important;
    box-shadow: none !important;
  }

  button.items:hover {
    background: var(--brand-color-two);
    color: var(--brand-color);
    border: none;
  }
</style>
