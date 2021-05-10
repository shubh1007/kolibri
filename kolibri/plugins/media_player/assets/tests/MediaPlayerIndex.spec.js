import MediaPlayerIndex from '../src/views/MediaPlayerIndex';

const { methods } = MediaPlayerIndex;

describe('updateProgress', () => {
  let context = {};

  beforeEach(() => {
    context = {
      $emit: jest.fn(),
      durationBasedProgress: 0.1,
    };
  });

  it('should be able to calculate progress using time-based tracking by default', () => {
    methods.updateProgress.call(context);

    expect(context.$emit.mock.calls[0][0]).toBe('updateProgress');
    expect(context.$emit.mock.calls[0][1]).toBe(0.1);
  });
});
