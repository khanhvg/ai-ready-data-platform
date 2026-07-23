const EMPTY_REGISTRY = Object.freeze({
  authorityKind: 'unadmitted',
  descriptors: Object.freeze([]),
  source: Object.freeze({
    validatorsInvoked: Object.freeze([]),
    releasedInputCount: 0
  })
});

export function createReleasedLearningAdapter() {
  return Object.freeze({
    readRegistry() {
      return EMPTY_REGISTRY;
    },
    describeCapabilities() {
      return Object.freeze({
        readOnly: true,
        listLessons: false,
        getLesson: false,
        mutations: Object.freeze([])
      });
    }
  });
}
