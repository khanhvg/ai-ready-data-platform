import contractSet from '../../../../learning/contracts/learning-contract-set-v1.json' with {
  type: 'json'
};
import promotionManifest from '../../../../learning/manifests/promotion-trust-v1.json' with {
  type: 'json'
};
import promotionLesson from '../../../../learning/lessons/promotion-trust/lesson-v1.json' with {
  type: 'json'
};
import promotionLab from '../../../../learning/labs/promotion-trust/lab-v1.json' with {
  type: 'json'
};
import viteBinding from '../../../../learning/bindings/vite/promotion-trust-v1.json' with {
  type: 'json'
};

const RELEASED_INPUT_COUNT = 85;
const RELEASED_HASHES = Object.freeze({
  contractSet: '92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638',
  manifest: '553b97ed5dc44b77564ae50b1a2211205cbd1a759f3578e5e4dfcefef99044ac',
  lesson: '758c6fb1ad75b283c313536d61bee61655bba6d27a2e685825ca20a28c838675',
  lab: '89ece51f41a17821d3266d2ba1fb7680cb70b07c2e9c5566d473aac9978d42d8',
  binding: '03d2aa6bd9fa178e6075865364a8ae8b83ce548c42b450d1858b451b45d0d1d0'
});

function deepFreeze(value) {
  if (value && typeof value === 'object' && !Object.isFrozen(value)) {
    for (const child of Object.values(value)) deepFreeze(child);
    Object.freeze(value);
  }
  return value;
}

function assertReleasedShape() {
  const contractMember = (path) => contractSet.contracts.find((entry) => entry.path === path);
  const expected = [
    [contractSet.schemaVersion, 'learning-contract-set-v1'],
    [promotionManifest.schemaVersion, 'promotion-trust-learning-manifest-v1'],
    [promotionLesson.schemaVersion, 'lesson-v1'],
    [promotionLab.schemaVersion, 'lab-v1'],
    [viteBinding.schemaVersion, 'promotion-trust-vite-binding-v1'],
    [viteBinding.stageA.contractSet.sha256, RELEASED_HASHES.contractSet],
    [viteBinding.stageA.promotionManifest.sha256, RELEASED_HASHES.manifest],
    [promotionManifest.lesson.sha256, RELEASED_HASHES.lesson],
    [promotionManifest.lab.sha256, RELEASED_HASHES.lab],
    [
      contractMember('learning/lessons/promotion-trust/lesson-v1.json')?.contentSha256,
      RELEASED_HASHES.lesson
    ],
    [
      contractMember('learning/labs/promotion-trust/lab-v1.json')?.contentSha256,
      RELEASED_HASHES.lab
    ]
  ];
  if (expected.some(([actual, required]) => actual !== required)) {
    throw new Error('PORTAL_RELEASE_IDENTITY_MISMATCH');
  }
  if (
    promotionManifest.decision !== promotionLesson.decision.status ||
    viteBinding.decision !== promotionLesson.decision.status ||
    promotionLab.lessonId !== promotionLesson.id
  ) {
    throw new Error('PORTAL_DESCRIPTOR_AUTHORITY_FORBIDDEN');
  }
}

function buildReleasedRegistry() {
  assertReleasedShape();
  const sourceGrains = viteBinding.grainBindings.map((binding) => {
    const source = promotionManifest.sources.find(({ grain }) => grain === binding.stageAGrain);
    if (!source) throw new Error('PORTAL_DESCRIPTOR_AUTHORITY_FORBIDDEN');
    return {
      id: binding.stageAGrain,
      displayId: binding.viteGrain,
      keys: [...binding.viteKeys],
      sourceKeys: [...source.keys],
      aliases: binding.aliases.map(({ from, to, kind }) => ({ from, to, kind }))
    };
  });
  const lesson = {
    ...promotionLesson,
    titleVi: 'Độ tin cậy của quyết định khuyến mãi',
    summaryVi: 'Đánh giá bằng chứng mà không tự suy diễn một grain chung.',
    sourceGrains,
    limitations: promotionManifest.limitations.map(({ id, statement }) => ({ id, statement })),
    controlledFailure: {
      available: false,
      trigger: promotionLab.controlledFailure.trigger,
      symptom: promotionLab.controlledFailure.symptom
    }
  };
  return deepFreeze({
    authorityKind: 'released',
    registryType: 'ReleasedPortalDescriptorRegistry',
    source: {
      contractSetVersion: contractSet.schemaVersion,
      contractSetSha256: RELEASED_HASHES.contractSet,
      validatorsInvoked: [
        'learning-contracts-check',
        'lesson-check',
        'api-contracts-check'
      ],
      releasedInputCount: RELEASED_INPUT_COUNT,
      hashes: RELEASED_HASHES
    },
    binding: viteBinding,
    descriptors: [
      {
        id: promotionManifest.manifestId,
        title: 'Bằng chứng quyết định khuyến mãi',
        presentationOnly: true,
        lessons: [lesson]
      }
    ]
  });
}

const RELEASED_REGISTRY = buildReleasedRegistry();
const NEGATIVE_CAPABILITIES = {
  readOnly: true,
  listLessons: true,
  getLesson: true,
  mutations: Object.freeze([]),
  runner: Object.freeze({ state: 'unavailable', controlledFailure: false }),
  progress: false,
  completion: false
};
const CAPABILITIES = new Proxy(NEGATIVE_CAPABILITIES, {
  has(target, property) {
    if (property === 'progress' || property === 'completion') return false;
    return Reflect.has(target, property);
  }
});

export function createReleasedLearningAdapter(options = {}) {
  if (
    options.descriptorMutation &&
    Object.keys(options.descriptorMutation).length > 0
  ) {
    throw new Error('PORTAL_DESCRIPTOR_AUTHORITY_FORBIDDEN');
  }
  if (
    options.protectedByteOverrides &&
    Object.keys(options.protectedByteOverrides).length > 0
  ) {
    throw new Error('PORTAL_RELEASE_IDENTITY_MISMATCH');
  }
  return Object.freeze({
    readRegistry() {
      return RELEASED_REGISTRY;
    },
    describeCapabilities() {
      return CAPABILITIES;
    }
  });
}
