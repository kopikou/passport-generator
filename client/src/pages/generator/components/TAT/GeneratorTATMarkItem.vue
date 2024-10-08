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
  },
})

const main = ref('')
const about = ref('')

const great = ref('')
const good = ref('')
const satisfactorily = ref('')
const unsatisfactory = ref('')

async function saveData() {
  $q.loading.show("Сохранение данных")
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: `tat_${props.type}`,
    value: {
      "main": main.value,
      "about": about.value,
      "great": great.value,
      "good": good.value,
      "satisfactorily": satisfactorily.value,
      "unsatisfactory": unsatisfactory.value,

    }
  })
  let key = _.findKey(additionalInfo.value, (x) => x.id == r.data.id)
  if (key === undefined) {
    additionalInfo.value.push(r.data)
  } else {
    _.set(additionalInfo.value, `[${key}].value['main']`, r.data.value['main'])
    _.set(additionalInfo.value, `[${key}].value['about']`, r.data.value['about'])
    _.set(additionalInfo.value, `[${key}].value['great']`, r.data.value['great'])
    _.set(additionalInfo.value, `[${key}].value['good']`, r.data.value['good'])
    _.set(additionalInfo.value, `[${key}].value['satisfactorily']`, r.data.value['satisfactorily'])
    _.set(additionalInfo.value, `[${key}].value['unsatisfactory']`, r.data.value['unsatisfactory'])
  }
  $q.loading.hide()
}

watch(additionalInfo, () => {
  main.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['main']
  about.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['about']
  great.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['great']
  good.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['good']
  satisfactorily.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['satisfactorily']
  unsatisfactory.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['unsatisfactory']
})

onBeforeMount(() => {
  main.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['main']
  about.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['about']
  great.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['great']
  good.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['good']
  satisfactorily.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['satisfactorily']
  unsatisfactory.value = _.filter(additionalInfo.value, (x) => x.type == `tat_${props.type}`)[0]?.value['unsatisfactory']
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
              label="Отлично"
              type="textarea"
              filled
              stack-label
              v-model="great"
              class="col q-mr-sm"
            />
            <q-input
              label="Хорошо"
              type="textarea"
              filled
              stack-label
              v-model="good"
              class="col q-ml-sm"
            />
          </div>
          <div class="row justify-between">
            <q-input
              label="Удовлетворительно"
              type="textarea"
              filled
              stack-label
              v-model="satisfactorily"
              class="col q-mr-sm"
            />
            <q-input
              label="Неудовлетворительно"
              type="textarea"
              filled
              stack-label
              v-model="unsatisfactory"
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
