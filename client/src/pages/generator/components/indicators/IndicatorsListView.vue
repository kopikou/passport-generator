<script setup lang="ts">

import {PlanIndicatorData} from "src/types";
import {onBeforeMount, ref} from "vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _ from "lodash";

const $q = useQuasar()
const generatorViewStore = useGeneratorViewStore();

const{
  disabled,
}=storeToRefs(generatorViewStore)

const props = defineProps({
  data: {
    type: Object as () => PlanIndicatorData,
    required: true,
  }
})

const know = ref(null)
const able = ref(null)
const own = ref(null)
const criteria = ref(null)
const methods = ref(null)

async function saveData() {
  $q.loading.show({message: "Сохранение"})
  let r = await api.post('/api/generator/save-discipline-indicator/', {
    indicator_id: props.data.id,
    planlineid_id: props.data.planlineid_id,
    know: know.value,
    able: able.value,
    own: own.value,
    criteria: criteria.value,
    methods: methods.value,
  }).then((v) => {
    $q.notify({
      message: "Данные <span class='text-bold'>о компетенциях</span> сохранены!",
      color: "secondary",
      position: "bottom",
      html: true,
    })
    props.data.discipline_indicator[0] = v.data
  }, (rej) => {
    $q.notify({
      message: "Данные <span class='text-bold'>о компетенциях</span> не сохранены!",
      color: "negative",
      position: "bottom",
      html: true,
    })
  })

  $q.loading.hide()
}

onBeforeMount(() => {
  if (props.data.discipline_indicator.length != 0) {
    know.value = props.data.discipline_indicator[0].know || null
    able.value = props.data.discipline_indicator[0].able || null
    own.value = props.data.discipline_indicator[0].own || null
    criteria.value = props.data.discipline_indicator[0].criteria || null
    methods.value = props.data.discipline_indicator[0].methods || null
  }
})

</script>

<template>
  <div class="q-pa-sm">
<!--    <span class="text-subtitle1">{{ data.indicator_index }} {{ data.indicator }}</span>-->
    <div class="indicators-form row justify-between q-gutter-md">
      <q-input
        filled
        label="Знать"
        stack-label
        type="textarea"
        class="col"
        v-model="know"
        :readonly="disabled"
        debounce="1000"
        @update:modelValue="saveData"
      />
      <q-input
        filled
        label="Уметь"
        stack-label
        type="textarea"
        class="col"
        v-model="able"
        :readonly="disabled"
        debounce="1000"
        @update:modelValue="saveData"
      />
      <q-input
        filled
        label="Владеть"
        stack-label
        type="textarea"
        class="col"
        v-model="own"
        :readonly="disabled"
        debounce="1000"
        @update:modelValue="saveData"
      />
      <q-input
        filled
        label="Критерии оценивания"
        stack-label
        type="textarea"
        class="col"
        v-model="criteria"
        :readonly="disabled"
        debounce="1000"
        @update:modelValue="saveData"
      />
      <q-input
        filled
        label="Средства (методы) оценивания промежуточной аттестации"
        stack-label
        type="textarea"
        class="col"
        v-model="methods"
        :readonly="disabled"
        debounce="1000"
        @update:modelValue="saveData"
      />
    </div>
<!--    <div class="flex justify-start q-mt-md">-->
<!--      <q-btn label="Сохранить" color="primary" @click="saveData" v-show="!disabled"/>-->
<!--    </div>-->
  </div>
</template>

<style scoped lang="scss">
.indicators-form {
  > label {
    flex-basis: 400px;
  }
}
</style>
