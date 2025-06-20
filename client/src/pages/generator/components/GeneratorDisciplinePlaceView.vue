<script setup lang="ts">

import {computed, onBeforeMount, ref, watch, watchEffect} from "vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _ from "lodash";
import QSelectFilterable from "components/QSelectFilterable.vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";

const $q = useQuasar()
const generatorViewStore = useGeneratorViewStore();

const {
  otherDiscipline,
  activeRpdId,
  disciplinePlace,
  additionalInfo,
  disabled,
  semesterYearLabel,
  semestersDataNum
} = storeToRefs(generatorViewStore)

const precedence = ref([])
const subsequent = ref([])

const filteredOthderDiscipline = computed(() => {
  const data = _(otherDiscipline.value).map(x => ({
    ...x, dis: `${x.dis} / ${(x.semesters || []).join(", ")} ${semesterYearLabel.value}`
  })).orderBy(x => [(x.semesters || [])[0], x.dis]).value()
  data.push({disid: 0, dis: 'Нет', semesters: [0]})
  return data
})


const filteredOtherDisciplinePrevious = computed(() => {
  return filteredOthderDiscipline.value.filter(x => _.min(x.semesters) <= _.min(semestersDataNum.value))
})


const filteredOtherDisciplineNext = computed(() => {
  return filteredOthderDiscipline.value.filter(x => _.min(x.semesters) >= _.min(semestersDataNum.value))
})

async function savePrecSubDiscipline() {
  if (generatorViewStore.abortGetDataController)
    generatorViewStore.abortGetDataController.abort()

  // $q.loading.show({message: "Сохранение"})
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: "disciplinePlace",
    value: {
      "precedence": precedence.value,
      "subsequent": subsequent.value,
    }
  })
  if (r.status == 200) {
    $q.notify({
      message: "Данные <span class='text-bold'>о месте дисциплины в структуре ООП</span> сохранены!",
      color: "secondary",
      position: "bottom-right",
      html: true,
    })

    // let key = _.findKey(additionalInfo.value, (x) => x.id == r.data.id)
    // if (key) {
    //   _.set(additionalInfo.value, `[${key}].value.precedence`, precedence.value)
    //   _.set(additionalInfo.value, `[${key}].value.subsequent`, subsequent.value)
    // } else {
    //   additionalInfo.value.push({
    //     id: r.data.id,
    //     planlineslink_id: activeRpdId.value,
    //     type: 'disciplinePlace',
    //     value: {
    //       "precedence": precedence.value,
    //       "subsequent": subsequent.value,
    //     }
    //   })
    // }
    await generatorViewStore.getData()
    generatorViewStore.checkErrors()

  } else {
    $q.notify({
      message: "Данные <span class='text-bold'>о месте дисциплины в структуре ООП</span> не сохранены!",
      color: "negative",
      position: "bottom-right",
      html: true,
    })

    // $q.loading.hide()
  }
}

watch(disciplinePlace, () => {
  precedence.value = disciplinePlace.value[0]?.value['precedence'] || []
  subsequent.value = disciplinePlace.value[0]?.value['subsequent'] || []
}, {
  immediate: true
})

</script>

<template>
  <div class="q-px-md">
      <span class="text-h6">Место дисциплины в структуре ООП</span>
      <p></p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-select-filterable
        label="Обеспечивающие (предшествующие) дисциплины и практики"
        v-model="precedence"
        option-label="dis"
        option-value="disid"
        stack-label
        filled
        use-chips
        multiple
        map-options
        emit-value
        :options="filteredOtherDisciplinePrevious"
        :readonly="disabled"
        @update:modelValue="savePrecSubDiscipline"
      />
      <br/>
      <q-select-filterable
        label="Обеспечиваемые (последующие) дисциплины и практики"
        v-model="subsequent"
        option-label="dis"
        option-value="disid"
        stack-label
        filled
        use-chips
        multiple
        map-options
        emit-value
        :options="filteredOtherDisciplineNext"
        :readonly="disabled"
        @update:modelValue="savePrecSubDiscipline"
      />
      <!--      <q-btn label="Сохранить" color="primary" class="q-mt-sm" @click="savePrecSubDiscipline" v-show="!disabled"/>-->
  </div>
</template>

<style scoped>

</style>
