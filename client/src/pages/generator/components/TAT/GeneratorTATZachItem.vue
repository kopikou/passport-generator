<script setup lang="ts">

import {useQuasar} from "quasar";
import {storeToRefs} from "pinia";
import useGeneratorViewStore from "stores/generatorViewStore";
import {onBeforeMount, ref, watch} from "vue";
import _ from "lodash";
import {api} from "boot/axios";

const generatorViewStore = useGeneratorViewStore();
const $q = useQuasar()
const {
  activeRpdId,
  additionalInfo,
} = storeToRefs(generatorViewStore)

const props = defineProps({
  title: {
    required: true,
  },
  type: {
    required: true,
  }
})

const main = ref('')
const about = ref('')

const passed = ref('')
const unpassed = ref('')

async function saveData() {
  $q.loading.show("Сохранение данных")
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: `tat_${props.type}`,
    value: {
      "main": main.value,
      "about": about.value,
      "passed": passed.value,
      "unpassed": unpassed.value,
    }
  })
  let key = _.findKey(additionalInfo.value, (x) => x.id == r.data.id)
  if (key === undefined) {
    additionalInfo.value.push(r.data)
  } else {
    _.set(additionalInfo.value, `[${key}].value['main']`, r.data.value['main'])
    _.set(additionalInfo.value, `[${key}].value['about']`, r.data.value['about'])
    _.set(additionalInfo.value, `[${key}].value['passed']`, r.data.value['passed'])
    _.set(additionalInfo.value, `[${key}].value['unpassed']`, r.data.value['unpassed'])
  }
  $q.loading.hide()
}

watch(additionalInfo, () => {
  main.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['main']
  about.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['about']
  passed.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['passed']
  unpassed.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['unpassed']
})

onBeforeMount(() => {
  main.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['main']
  about.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['about']
  passed.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['passed']
  unpassed.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['unpassed']
})

</script>

<template>
  <q-expansion-item
    :label=props.title
  >
    <q-card>
      <q-card-section>
        <div class="q-gutter-md">
          <q-input
            label="Основная информация"
            type="textarea"
            filled
            stack-label
            v-model="main"
          />
          <q-input
            label="Описание процедуры"
            type="textarea"
            filled
            stack-label
            v-model="about"
          />
          <p class="text-subtitle1">Критерии оценивания</p>
          <div class="row justify-between">
            <q-input
              label="Зачтено"
              type="textarea"
              filled
              stack-label
              v-model="passed"
              class="col q-mr-sm"
            />
            <q-input
              label="Не зачтено"
              type="textarea"
              filled
              stack-label
              v-model="unpassed"
              class="col q-ml-sm"
            />
          </div>

          <q-btn
            label="Сохранить"
            color="primary"
            @click="saveData"
          />
        </div>
      </q-card-section>
    </q-card>
  </q-expansion-item>
  <q-separator/>
</template>

<style scoped>
</style>
