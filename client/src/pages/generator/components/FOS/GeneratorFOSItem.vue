<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {useQuasar} from "quasar";
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
  title: {},
  type: {
    required: true,
  }
})

const about = ref('')
const criteria = ref('')

async function saveData() {
  $q.loading.show("Сохранение данных")
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: `fos_${props.type}`,
    value: {
      "about": about.value,
      "criteria": criteria.value,
    }
  })
  let key = _.findKey(additionalInfo.value, (x) => x.id == r.data.id)
  if (key === undefined) {
    additionalInfo.value.push(r.data)
  } else {
    _.set(additionalInfo.value, `[${key}].value['about']`, r.data.value['about'])
    _.set(additionalInfo.value, `[${key}].value['criteria']`, r.data.value['criteria'])
  }
  $q.loading.hide()
}

watch(additionalInfo, () => {
  about.value = _.filter(additionalInfo.value, (x) => x.type == `fos_${props.type}`)[0]?.value['about']
  criteria.value = _.filter(additionalInfo.value, (x) => x.type == `fos_${props.type}`)[0]?.value['criteria']
})

onBeforeMount(() => {
  about.value = _.filter(additionalInfo.value, (x) => x.type == `fos_${props.type}`)[0]?.value['about']
  criteria.value = _.filter(additionalInfo.value, (x) => x.type == `fos_${props.type}`)[0]?.value['criteria']
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
            label="Описание процедуры"
            type="textarea"
            filled
            stack-label
            v-model="about"
          />
          <q-input
            label="Критерии оценивания"
            type="textarea"
            filled
            stack-label
            v-model="criteria"
          />
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
